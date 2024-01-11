import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name, get_file_name_with_ext
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    images_path = "/home/alex/DATASETS/TODO/SYNTHIA-PANO/SYNTHIA-PANO/RGB"
    masks_path = "/home/alex/DATASETS/TODO/SYNTHIA-PANO/SYNTHIA-PANO/LABELS"
    batch_size = 5
    ds_name = "ds"
    images_folder = "RGB"
    masks_folder = "LABELS"

    images_ext = "_pano_"
    masks_ext = "_label_"

    def create_ann(image_path):
        labels = []

        subfolder_value = image_path.split("/")[-2]
        subfolder = sly.Tag(subfolder_meta, value=subfolder_value)

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 760  # image_np.shape[0]
        img_wight = 3340  # image_np.shape[1]

        mask_path = image_path.replace(images_folder, masks_folder).replace(images_ext, masks_ext)
        mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
        unique_pixels = np.unique(mask_np)
        for pixel in unique_pixels:
            obj_class = pixel_to_class.get(pixel)
            mask = mask_np == pixel
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                bitmap = sly.Bitmap(data=obj_mask)
                if bitmap.area > 50:
                    label = sly.Label(bitmap, obj_class)
                    labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[subfolder])

    pixel_to_class = {
        0: sly.ObjClass("void", sly.Bitmap, color=(0, 0, 0)),
        1: sly.ObjClass("sky", sly.Bitmap, color=(128, 128, 128)),
        2: sly.ObjClass("building", sly.Bitmap, color=(128, 0, 0)),
        3: sly.ObjClass("road", sly.Bitmap, color=(128, 64, 128)),
        4: sly.ObjClass("sidewalk", sly.Bitmap, color=(0, 0, 192)),
        5: sly.ObjClass("fence", sly.Bitmap, color=(64, 64, 128)),
        6: sly.ObjClass("vegetation", sly.Bitmap, color=(128, 128, 0)),
        7: sly.ObjClass("pole", sly.Bitmap, color=(192, 192, 128)),
        8: sly.ObjClass("car", sly.Bitmap, color=(64, 0, 128)),
        9: sly.ObjClass("traffic sign", sly.Bitmap, color=(192, 128, 128)),
        10: sly.ObjClass("pedestrian", sly.Bitmap, color=(64, 64, 0)),
        11: sly.ObjClass("bicycle", sly.Bitmap, color=(0, 128, 192)),
        12: sly.ObjClass("landmarking", sly.Bitmap, color=(0, 172, 0)),
        15: sly.ObjClass("traffic light", sly.Bitmap, color=(0, 128, 128)),
    }

    subfolder_meta = sly.TagMeta("subfolder", sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=list(pixel_to_class.values()), tag_metas=[subfolder_meta])
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = glob.glob(images_path + "/*/*.png")

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))

    return project
