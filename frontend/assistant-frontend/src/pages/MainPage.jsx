import "@mohayonao/web-audio-api-shim";
import axios from "axios";
import React from "react";
import { Button, Container, Row } from "react-bootstrap";
import { useNavigate } from "react-router";
import Header from "../components/Header";
// import PcmUtil from 'pcm-util';
import { observer } from "mobx-react";
import { useEffect, useState } from "react";
import ResponseResult from "../components/ResponseResult";
import TextRequest from "../modules/MakeRequests/TextRequest";
import VoiceRecorderWAV from "../modules/MakeRequests/VoiceRecorderWAV";
import store from "../store/Store";
import transition from "../transition";
var options = {
	audioBitsPerSecond: 48000,
};
const token = localStorage.getItem("authToken");
axios.defaults.headers.common["Authorization"] = token
	? `Token ${token}`
	: null;
const MainPage = observer((props) => {
	const [isModalResponseResultActive, setIsModalResponseResultActive] = useState(false);
	const [showResultButton, setShowResultButton] = useState(false);
	const [showVoiceInput, setShowVoiceInput] = useState(true);
	const [showTextInput, setShowTextInput] = useState(false);

	function handleVoiceInput () {
		setShowResultButton(false)
		setShowVoiceInput(true)
		setShowTextInput(false)
	}
	function handleTextInput () {
		setShowTextInput(true)
		setShowResultButton(false)
		setShowVoiceInput(false)
	}

  function handleModalResponseResultActiveOpen() {
		store.setCheckResult(true)
		setIsModalResponseResultActive(true);
	}
	function handleModalResponseResultActiveClose() {
		setShowResultButton(true)
		store.setCheckResult(false)
		setIsModalResponseResultActive(false);
	}
	const navigate = useNavigate();
	useEffect(() => {
		// store.getHistoryAction().then(() => {console.log("links: " + store.links);});
		// store.getHistoryAction()
		
		// store.checkAuth().then(() => {
		// 	if (store.isAuthenticated === false) {
		// 		navigate("/");
		// 	} else {
		// 		navigate("/MainPage");
		// 	}
		// });
		console.log("isAuthenticated: " + store.isAuthenticated);
	}, []);
	return (
		<div>
			<Header />
			<Container>
				<Row className="d-flex justify-content-center align-items-center">
					<div className="btn-group w-50 p-2 m-3" role="group" aria-label="Basic example">
						<button type="button" className={showVoiceInput ? "btn btn-outline-primary active" : "btn btn-outline-primary "} onClick={handleVoiceInput}>Голосовой ввод</button>
						<button type="button" className={showTextInput ? "btn btn-outline-primary active" : "btn btn-outline-primary"} onClick={handleTextInput}>Текстовый ввод</button>
					</div>
				</Row>
				{showVoiceInput && <Row
					style={{
						backgroundColor: "#EFEFEF",
						margin: "20px",
						borderRadius: "20px",
					}}
					className="d-flex justify-content-center align-items-center"
				>
					<h2 className="text-center mt-5">Введите голосовую команду</h2>
					<VoiceRecorderWAV getHistory={store.getHistory}/>
					{false && (
						<Button onClick={handleModalResponseResultActiveOpen} className="w-25 p-1 mb-3 btn-secondary">
						Подробнее о результате
					</Button>
					)}
					
				</Row>}

				{showTextInput && <Row
					style={{
						backgroundColor: "#EFEFEF",
						margin: "20px",
						borderRadius: "20px",
					}}
					className="d-flex justify-content-center align-items-center"
				>
					{showTextInput && <TextRequest />}
					{showResultButton && (
						<Button onClick={handleModalResponseResultActiveOpen} className="w-25 p-1 mb-3 btn-secondary">
						Подробнее о результате
					</Button>
					)}
				</Row>}
				
				

				{/* <Row
					style={{
						backgroundColor: "#EFEFEF",
						margin: "20px",
						borderRadius: "20px",
					}}
					className="d-flex justify-content-center align-items-center"
				>
					<h5 className="text-center mt-3">История запросов</h5>
					{store.links ? (
						<HistoryOfRequests links={store.links} />
					) : (
						<div className="d-flex justify-content-center align-items-center">
							<p>Нет ранее выполненных запросов</p>
						</div>
					)}
				</Row> */}
				<ResponseResult
						showModal={store.checkResult}
						handleModalClose={handleModalResponseResultActiveClose}
					/>
			</Container>
		</div>
	);
});

export default transition(MainPage);
