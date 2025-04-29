import axios from "axios";
import { observer } from "mobx-react";
import React, { useEffect, useState } from "react";
import { Button, Container, Form, FormControl, Row } from "react-bootstrap";
import LoadingOverlay from "../../components/Auth/LoadingOverlay";
import store from "../../store/Store";
const TextRequest = observer(() => {
	const [text, setText] = useState("");
	const [loading, setLoading] = useState(false);
	const [checkError, setCheckError] = useState(false)
	const [uploadRequest, setUploadRequest] = useState(false);
	useEffect(() => {
		// store.getHistory();
	}, []); // Пустой массив зависимостей, чтобы useEffect сработал только один раз при монтировании компонента

	const handleTextChange = (e) => {
		setText(e.target.value);
	};

	const uploadTextRequest = (request) => {
		setLoading(true);
		axios
			.post(`${process.env.REACT_APP_URL_BACKEND}upload_text/`, {
				headers: {
					Authorization: `Token ${localStorage.getItem("authToken")}`,
				},
				textRequest: request,
			})
			.then((response) => {
				
				console.log("Текстовый вопрос загружен, ответ: ", response.data);
				setLoading(false)
				if (response.data.url === 'null') {
					
					store.setResponse(response.data.text)
					store.setCheckResult(false)
					setCheckError(true)
				}
				else {
					setUploadRequest(true)
					store.setCheckResult(true)
					store.setFiltersResponse(response.data.response_with_filters)
					store.setResponse(response.data)
					console.log('url: ' + response.data.url)
					setCheckError(false)
					
					// window.open(response.data.url, "_blank");
				}
				store.getHistoryAction();
				
			})
			.catch((error) => {
				setLoading(false)
				setCheckError(true)
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
						className="m-2 p-3 text-lg-center"
					/>
					
				</Form>
				<Button
						variant="primary"
						className=" w-25 text-xl-center btn-lg"
						onClick={() => uploadTextRequest(text)}
					>
						Отправить запрос
					</Button>
			</Row>

			{/* {uploadRequest && <Row>
					{store.filtersResponse.filters.map((item, index) => (
						<>
							<p key={index}>
								{item.initial_name}
							</p>
							<p key={index}>
								{item.initial_value}
							</p>
						</>
						
					))}
					<h5>
						{store.filtersResponse.dashboards.value}
					</h5>
					<h5>
						{store.filtersResponse.command}
					</h5>
				</Row>} */}

			{checkError && <Row>
				<h5 className="text-center">
							Запрос: "{store.response.text}"
						</h5>
						<h5 className="text-center" style={{ color: "red" }}>
							Не удалось составить запрос, повторите попытку
						</h5>
			</Row>}
			
			{loading && <LoadingOverlay show={loading} />}
		</Container>
	);
});

export default TextRequest;
