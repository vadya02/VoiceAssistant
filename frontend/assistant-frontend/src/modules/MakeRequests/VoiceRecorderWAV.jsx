import axios from "axios";
import MicRecorder from "mic-recorder-to-mp3";
import { observer } from "mobx-react";
import React, { useEffect, useState } from "react";
import { Button, Row } from "react-bootstrap";
import { VoiceVisualizer, useVoiceVisualizer } from "react-voice-visualizer";
import "../../assets/css/style.css";
import LoadingOverlay from "../../components/Auth/LoadingOverlay";
import store from "../../store/Store";
const VoiceRecorderWAV = observer(({ getHistory }) => {
	const [isRecording, setIsRecording] = useState(false);
	const [isUpload, setIsUpload] = useState(false);
	const [recorder, setRecorder] = useState(new MicRecorder({ bitRate: 128 }));
	const [audioBlob, setAudioBlob] = useState(null);
	const [checkResult, setCheckResult] = useState(false);
	const [loading, setLoading] = useState(false);
	const [nullUrl, setNullUrl] = useState(false);
	// const { response, setResponse } = store;


	// const stopRecording = async () => {
	// 	setIsRecording(false);
	// 	recorder
	// 		.stop()
	// 		.getMp3()
	// 		.then(([buffer, blob]) => {
	// 			console.log("Записанный blob: " + blob);
	// 			setAudioBlob(blob);
	// 			uploadAudio(blob);
	// 			console.log("Записанный audio: " + blob);
	// 		})
	// 		.then(() => {
	// 			console.log("stop record");
	// 		})
	// 		.catch((e) => console.log(e));
	// };

	const onStopRecording = () => {
		console.log("blob: " + recordedBlob);
		uploadAudio(recordedBlob);
	};


	const onClearCanvas = () => {
		setNullUrl(false)
		setCheckResult(false)
	};

	const onStartRecording = () => {
		// document.querySelector('voice-visualizer__btn ').textContent = 'Очистить';
	};

	const recorderControls = useVoiceVisualizer({onClearCanvas, onStartRecording});
	const { recordedBlob, error, audioRef } = recorderControls;

	useEffect(() => {
		if (!recordedBlob) return;

		console.log(recordedBlob);
		uploadAudio(recordedBlob);
		console.log(recorderControls.stopRecording);
	}, [recordedBlob, error]);

	useEffect(() => {
		if (!error) return;

		console.error(error);
	}, [error]);

	// const startRecording = async () => {
	// 	console.log("start record");

	// 	setIsRecording(true);
	// 	recorder
	// 		.start()
	// 		.then(() => {
	// 			// recording started
	// 		})
	// 		.catch((e) => console.error(e));
	// };

	const uploadAudio = (audioBlob) => {
		console.log("blob: " + audioBlob);
		console.log("uploading");
		setLoading(true);
		setNullUrl(false);
		setIsUpload(false);
		try {
			const formData = new FormData();
			const token = localStorage.getItem("authToken");
			formData.append("audio_file", audioBlob, "recording.wav");
			console.log("Записанный blob: " + audioBlob);
			console.log("Записанный formData: " + formData);

			axios
				.post("http://127.0.0.1:8000/upload_audio_file_mp3/", formData, {
					headers: {
						"Content-Type": "multipart/form-data",
						Authorization: `Token ${localStorage.getItem("authToken")}`,
					},
				})
				.then((response) => {
					store.setResponse(response.data);

					if (response.data.url === 'null') {
						store.setCheckResult(false)
						store.setResponse(response.data);
						setNullUrl(true);
					} else {
						store.setCheckResult(true)
						store.setFiltersResponse(response.data.response_with_filters)
						console.log("response: " + response.data.url);
						setNullUrl(false);

						// window.open(response.data.url, "_blank");
					}
					store.getHistoryAction();
					setLoading(false);
					setCheckResult(true);
				})
				.catch((error) => {
					setLoading(false);
					setNullUrl(true);

					// Обработка ошибок
					console.error("Error posting data:", error);
				});

			// Обработайте успешную загрузку аудио
		} catch (error) {
			console.log(error);
			// Обработайте ошибку
		}
	};

	return (
		<div className="">
			<Row className="d-flex justify-content-center align-items-center">
				<VoiceVisualizer
					ref={audioRef}
					height={180}
					mainBarColor="black"
					controls={recorderControls}
					barWidth={5}
				/>
				{/* {recordedBlob && (
					<AudioVisualizer
						ref={audioRef}
						blob={recordedBlob}
						width={500}
						height={75}
						barWidth={1}
						gap={0}
						barColor={"#f76565"}
					/>
				)} */}

				{/* <div
					className={isRecording ? "microphone-stop" : "microphone-record"}
					onClick={
						isRecording
							? () => {
									stopRecording();
							  }
							: () => {
									startRecording();
							  }
					}
				>
					<FaMicrophone className="microphone-icon" />
				</div> */}

				<div className={isRecording ? "recording-animation" : ""}></div>
				{isUpload && (
					<Button
						className="w-25 m-2"
						variant="outline-primary"
						onClick={uploadAudio}
					>
						Отправить запрос
					</Button>
				)}
			</Row>
			<Row className="d-flex justify-content-center align-items-center p-2">
				{checkResult && !nullUrl && (
					<h5 className="text-center">
						Распознанный текст: "{store.response.text}"
					</h5>
				)}
			</Row>
			<Row className="d-flex justify-content-center align-items-center p-2">
				{nullUrl && (
					<>
						<h5 className="text-center">
							Распознанный текст: "{store.response.text}"
						</h5>
						<h5 className="text-center" style={{ color: "red" }}>
							Не удалось составить запрос, повторите попытку
						</h5>
					</>
				)}
			</Row>

			{loading && <LoadingOverlay show={loading} />}
		</div>
	);
});

export default VoiceRecorderWAV;
