// import 'bootstrap/dist/css/bootstrap.min.css';
// import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import axios from "axios";
import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";

const ModalReg = (props) => {
	const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
	const [email, setEmail] = useState("");
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const [checkPassword, setChechPassword] = useState(true);
	const [checkPasswordCommon, setCheckPasswordCommon] = useState(true);
	const [checkLogin, setCheckLogin] = useState(true);
	const handleSubmit = (event) => {
		event.preventDefault(); // Предотвращаем стандартное поведение формы
		if (!passwordRegex.test(password)) {
			setChechPassword(false);
		} else {
			setChechPassword(true);
			const userData = {
				email: email,
				username: username,
				password: password,
				re_password: confirmPassword,
			};
			console.log(userData);
			const jsonString = JSON.stringify(userData);
			sendDataToServer(jsonString);
		}
		// Создайте объект с данными для отправки на сервер
	};

	const sendDataToServer = (data) => {
		axios({
			method: "post",
			url: `${process.env.REACT_APP_URL_BACKEND}auth/users/`,
			data: data,
			headers: {
				"Content-Type": "application/json",
			},
		})
			.then((response) => {
				// Обработка успешного ответа
				setCheckLogin(true);
				console.log("Успешная регистрация:", response.data);
				alert("Регистрация прошла успешно");
				props.handleModalClose();
			})
			.catch((error) => {
				// Обработка ошибки
				console.log(error.data);
				console.log(error.response.data); // Данные ошибки от сервера
				console.log(error.response.status); // Код состояния
				console.log(error.response.headers);
				console.log(error.response.data.password[0]);
				if (
					error.response.data.password[0] === "This password is too common."
				) {
					setCheckPasswordCommon(false);
				}
				// setUsername('')
				// setPassword('')
				// setConfirmPassword('')
				// console.log(response.data);
				console.error(error);
				if (
					error.response.data.username ===
					"A user with that username already exists."
				) {
					setCheckLogin(false);
				}
			});
	};

	const handleClick = () => {
		props.openAuthClick();
		props.handleModalClose();
	};

	return (
		<div className="">
			<Modal
				show={props.showModal}
				onHide={props.handleModalClose}
				size="md"
				aria-labelledby="contained-modal-title-vcenter"
				centered
			>
        <div className=" modal-content bg-transparent">
        <Modal.Body
					className="bg-dark text-light rounded-5"
					
				>
          <Modal.Title className="text-center mt-3 fw-normal fs-2 mb-2 text-uppercase">Регистрация</Modal.Title>
					<Form onSubmit={handleSubmit} className="m-3">
						{/* Форма регистрации */}
						<Form.Group controlId="formBasicEmail" className="m-2">
							<Form.Label>Email адрес</Form.Label>
							<Form.Control
								type="email"
								placeholder="Введите email"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
                className="p-3"
							/>
						</Form.Group>
						<Form.Group controlId="formBasicUsername" className="m-2">
							<Form.Label>Логин</Form.Label>
							<Form.Control
								type="text"
								placeholder="Введите логин"
								value={username}
								onChange={(e) => setUsername(e.target.value)}
                className="p-3"
							/>
						</Form.Group>
						{!checkLogin && (
							<Form.Group
								style={{
									alignItems: "center",
									display: "flex",
									justifyContent: "center",
									color: "red",
								}}
							>
								<p>Пользователь с таким именем уже существует</p>
							</Form.Group>
						)}
						<Form.Group controlId="formBasicPassword" className="m-2">
							<Form.Label>Пароль</Form.Label>
							<Form.Control
								type="password"
								placeholder="Введите пароль"
								value={password}
								onChange={(e) => setPassword(e.target.value)}
                className="p-3"
							/>
						</Form.Group>
						{!checkPassword && (
							<Form.Group
								style={{
									alignItems: "center",
									display: "flex",
									justifyContent: "center",
									color: "red",
								}}
							>
								<p>
									Пароль должен состоять из букв и цифр, а также быть не короче
									8 символов
								</p>
							</Form.Group>
						)}
						{!checkPasswordCommon && (
							<Form.Group
								style={{
									alignItems: "center",
									display: "flex",
									justifyContent: "center",
									color: "red",
								}}
							>
								<p>Пароль небезопасен</p>
							</Form.Group>
						)}
						<Form.Group controlId="formBasicPassword" className="m-2">
							<Form.Label>Подтвердите пароль</Form.Label>
							<Form.Control
								type="password"
								placeholder="Введите пароль"
								value={confirmPassword}
								onChange={(e) => setConfirmPassword(e.target.value)}
                className="p-3"
							/>
						</Form.Group>
						{!checkPassword && (
							<Form.Group
								style={{
									alignItems: "center",
									display: "flex",
									justifyContent: "center",
									color: "red",
								}}
							>
								<p>
									Пароль должен состоять из букв и цифр, а также быть не короче
									8 символов
								</p>
							</Form.Group>
						)}
						<Form.Group className=" d-flex justify-content-center align-items-center "
							
						>
							<Button
								variant="primary"
								type="submit"
                className="px-5 m-3"
                size="lg "
							>
								Зарегистрироваться
							</Button>
						</Form.Group>
						<Form.Group
							style={{
								alignItems: "center",
								display: "flex",
								justifyContent: "center",
								margin: "5px",
							}}
						>
							<Form.Label>Уже зарегистрированы?</Form.Label>
							<Form.Label
								style={{ color: "#0D6EFD", cursor: "pointer" }}
								onClick={handleClick}
							>
								Войти
							</Form.Label>
						</Form.Group>
					</Form>
				</Modal.Body>
        </div>
				
			</Modal>
		</div>
	);
};

export default ModalReg;
