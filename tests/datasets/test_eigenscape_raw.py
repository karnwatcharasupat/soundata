import numpy as np

from tests.test_utils import run_clip_tests

from soundata import annotations
from soundata.datasets import eigenscape_raw


TEST_DATA_HOME = "tests/resources/sound_datasets/eigenscape_raw"


def test_clip():
    default_clipid = "Beach-01-Raw"
    dataset = eigenscape_raw.Dataset(TEST_DATA_HOME)
    clip = dataset.clip(default_clipid)

    expected_attributes = {
        "audio_path": (
            "tests/resources/sound_datasets/eigenscape_raw/Beach-01-Raw.wav"
        ),
        "clip_id": "Beach-01-Raw",
    }

    expected_property_types = {
        "audio": tuple,
        "tags": annotations.Tags,
        "location": str,
        "date": str,
        "time": str,
        "additional_information": str,
    }

    run_clip_tests(clip, expected_attributes, expected_property_types)


def test_load_audio():
    default_clipid = "Beach-01-Raw"
    dataset = eigenscape_raw.Dataset(TEST_DATA_HOME)
    clip = dataset.clip(default_clipid)
    audio_path = clip.audio_path
    audio, sr = eigenscape_raw.load_audio(audio_path)
    assert sr == 48000
    assert type(audio) is np.ndarray
    assert len(audio.shape) == 2  # check audio is loaded correctly
    assert audio.shape[0] == 32  # check audio is 32ch (HOA 4th order)
    assert audio.shape[1] == 48000 * 1.0  # Check audio duration is as expected


def test_load_tags():
    # dataset
    default_clipid = "Beach-01-Raw"
    dataset = eigenscape_raw.Dataset(TEST_DATA_HOME)
    clip = dataset.clip(default_clipid)
    assert len(clip.tags.labels) == 1
    assert clip.tags.labels[0] == "Beach"
    assert np.allclose([1.0], clip.tags.confidence)


def test_load_metadata():
    # dataset
    default_clipid = "Beach-01-Raw"
    dataset = eigenscape_raw.Dataset(TEST_DATA_HOME)
    clip = dataset.clip(default_clipid)
    assert clip.location == "Bridlington Beach"
    assert clip.time == "10:42"
    assert clip.date == "09/05/2017"
    assert clip.additional_information == ""


def test_to_jams():
    default_clipid = "Beach-01-Raw"
    dataset = eigenscape_raw.Dataset(TEST_DATA_HOME)
    clip = dataset.clip(default_clipid)
    jam = clip.to_jams()

    assert jam.validate()

    # Validate Tags
    tags = jam.search(namespace="tag_open")[0]["data"]
    assert len(tags) == 1
    assert tags[0].time == 0
    assert tags[0].duration == 1.0
    assert tags[0].value == "Beach"
    assert tags[0].confidence == 1

    # validate metadata
    assert jam.file_metadata.duration == 1.0
    assert jam.sandbox.location == "Bridlington Beach"
    assert jam.sandbox.time == "10:42"
    assert jam.sandbox.date == "09/05/2017"
    assert jam.annotations[0].annotation_metadata.data_source == "soundata"
