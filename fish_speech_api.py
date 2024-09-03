from gradio_client import Client, handle_file
import logging


async def fish_speech_api(message: str) -> str:
    """
    This function takes a message as input and returns a fish speech audio file.
    """
    client = Client("http://127.0.0.1:7862/")
    result = client.predict(
		    text=message,
		    enable_reference_audio=True,
		    reference_audio=handle_file('D:/rvcwebui/fish-speech/fake.wav'),
		    reference_text="人间灯火倒映湖中，她的渴望让静水泛起涟漪。若代价只是孤独，那就让这份愿望肆意流淌。流入她所注视的世间，也流入她如湖水般澄澈的目光。",
		    max_new_tokens=1024,
		    chunk_length=100,
		    top_p=0.7,
		    repetition_penalty=1.2,
		    temperature=0.7,
		    batch_infer_num=1,
		    if_load_asr_model=False,
		    api_name="/inference_wrapper"
    )
    result_file = result[1]['value']
    logging.info(f"Result file: {result_file}")
    return result_file
