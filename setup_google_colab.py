#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def download_file(url, file_path):
    print(url, file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    template = "wget '{}' -O '{}'"
    os.system(template.format(url, file_path))


def download_github_code(path):
    course = 'bayesian-methods-for-ml'
    branch = 'master'
    url = 'https://raw.githubusercontent.com/hse-aml/{}/{}/{}'
    file_path = path.rsplit("/")[-1]
    download_file(url.format(course, branch, path), file_path)


def load_data_week2():
    download_github_code("week2/w2_grader.py")
    download_github_code("week2/samples.npz")


def load_data_week4():
    download_github_code("week4/w4_grader.py")
    download_github_code("week4/adult_us_postprocessed.csv")


def load_data_week5():
    download_github_code("week5/w5_grader.py")
    download_github_code("week5/test_data.npz")


def load_data_week6():
    download_github_code("week6/w6_grader.py")


def load_data_final_project():
    download_github_code("week7_(final_project)/utils.py")
    download_file(
        "https://github.com/hse-aml/bayesian-methods-for-ml/"
        "releases/download/v0.1/CelebA_VAE_small_8.h5",
        "CelebA_VAE_small_8.h5"
    )
