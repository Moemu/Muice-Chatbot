from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import torch
import logging
import asyncio

class SpeechRecognitionPipeline:
    _model = None

    @classmethod
    def load_model(cls, model_path):
        logging.info("Loading speech recognition model...")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logging.info("Using device: {}".format(device))
        try:
            cls._model = AutoModel(
                                   model=model_path,
                                   trust_remote_code=True,
                                   device=str(device),
                                   disable_update=True
                                   )
        except Exception as e:
            if "Loading remote code failed: model, No module named 'model'" in str(e):
                try:
                    cls._model = AutoModel(
                                           model=model_path,
                                           trust_remote_code=False,
                                           device=str(device),
                                           disable_update=True
                                           )
                except Exception as e2:
                    logging.error("Failed to load speech recognition model: {}".format(e2))
                    raise e2 from e
            else:
                logging.error("Failed to load speech recognition model: {}".format(e))
                raise e
        logging.info("Model loaded successfully.")

    async def generate_speech(self, file_path):
        logging.info("Generating speech...")
        rec_result = self._model.generate(
                                          input=file_path,
                                          cache={},
                                          language="zh", # "auto", "zh", "en", "yue", "ja", "ko", "nospeech"
                                          batch_size_s=60,
                                          merge_vad=True,
                                          merge_length_s=15
                                          )
        rec_result = rich_transcription_postprocess(rec_result[0]["text"])
        logging.info(f"Speech generated : {rec_result}")
        return rec_result
