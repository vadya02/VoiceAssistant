import "@mohayonao/web-audio-api-shim";
import axios from "axios";
import React from "react";
import { Container, Row } from "react-bootstrap";
import { useNavigate } from "react-router";
import Header from "../components/Header";
// import PcmUtil from 'pcm-util';
import { observer } from "mobx-react";
import HistoryOfRequests from "../modules/History/HistoryOfRequests";
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
	const navigate = useNavigate();

	return (
		<div>
			<Header />
			<Container>
				<Row
					style={{
						backgroundColor: "#EFEFEF",
						margin: "20px",
						borderRadius: "20px",
					}}
					className="d-flex justify-content-center align-items-center"
				>
					<h2 className="text-center mt-5">Введите голосовую команду</h2>
					<VoiceRecorderWAV getHistory={store.getHistory} />
				</Row>
				<Row
					style={{
						backgroundColor: "#EFEFEF",
						margin: "20px",
						borderRadius: "20px",
					}}
					className="d-flex justify-content-center align-items-center"
				>
					<TextRequest/>
				</Row>

				<Row
					style={{
						backgroundColor: "#EFEFEF",
						margin: "20px",
						borderRadius: "20px",
					}}
					className="d-flex justify-content-center align-items-center"
				>
					<h5 className="text-center mt-3">История запросов</h5>
					{!store.links ? (
						<HistoryOfRequests links={store.links} />
					) : (
						<div className="d-flex justify-content-center align-items-center">
							<p>Нет ранее выполненных запросов</p>
						</div>
					)}
				</Row>
			</Container>
		</div>
	);
});

export default transition(MainPage);
