import axios from "axios";
import { observer } from "mobx-react";
import React, { useEffect, useState } from "react";
import { Button, Container, Form, FormControl, Row } from "react-bootstrap";
import store from "../../store/Store";
const TextRequest = observer(() => {
	const [text, setText] = useState("");

	useEffect(() => {
		store.getHistory();
	}, []); // Пустой массив зависимостей, чтобы useEffect сработал только один раз при монтировании компонента

	const handleTextChange = (e) => {
		setText(e.target.value);
	};

	const uploadTextRequest = (request) => {
		axios
			.post(`${process.env.REACT_APP_URL_BACKEND}upload_audio_text/`, {
				headers: {
					Authorization: `Token ${localStorage.getItem("authToken")}`,
				},
				textRequest: request,
			})
			.then((response) => {
				store.getHistory();
				console.log("Audio file uploaded successfully:", response.data);
				window.open(response.data.url, "_blank");
			})
			.catch((error) => {
				console.error("Error uploading audio file:", error);
			});
	};
	return (
		<Container>
			<Row
				style={{
					backgroundColor: "#EFEFEF",
					margin: "20px",
					borderRadius: "20px",
				}}
				className="d-flex justify-content-center align-items-center"
			>
				<h3 className="text-center m-2">Введите текстовую команду</h3>
				<Form className="d-flex justify-content-center align-items-center m-2">
					<FormControl
						type="text"
						placeholder={"Введите текстовый запрос"}
						value={text}
						onChange={handleTextChange}
						className="m-2"
					/>
					<Button
						variant="outline-primary"
						onClick={() => uploadTextRequest(text)}
					>
						Отправить
					</Button>
				</Form>
			</Row>
		</Container>
	);
});

export default TextRequest;
