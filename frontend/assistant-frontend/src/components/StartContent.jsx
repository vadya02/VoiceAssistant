import "bootstrap/dist/css/bootstrap.min.css";
import React, { useState } from "react";
import { Button, Col, Container, Image, Row } from "react-bootstrap";
import "../assets/css/style.css";
import StartIcon from "../assets/img/StartIcon.png";
import BackgroundImage from "../assets/img/background.jpg";
import store from "../store/Store";
import LoginModal from "./Auth/LoginModal";
function StartContent({}) {
	const [isModalAuthActive, setIsModalAuthActive] = useState(false);
	const [isModalRegActive, setIsModalRegActive] = useState(false);
	function handleModalAuthActiveOpen() {
		setIsModalAuthActive(true);
	}
	function handleModalAuthActiveClose() {
		setIsModalAuthActive(false);
	}
	function handleModalRegActiveOpen() {
		setIsModalRegActive(true);
	}
	function handleModalRegActiveClose() {
		setIsModalRegActive(false);
	}
	return (
		<div className="h-100">
			<Container
				fluid="true"
				className="d-flex align-items-center h-100"
				style={{
					backgroundImage: `url(${BackgroundImage})`,
					backgroundSize: "cover",
					backgroundPosition: "center",
				}}
			>
				<Row className="justify-content-center align-items-center d-flex m-lg-3">
					<Col md={6}>
						<Image src={StartIcon} fluid />
					</Col>
					<Col md={6} className="text-center mx-3">
						<h1>Голосовой помощник для Apache Superset</h1>
						<p>Стройте дашборды с помощью голосовых команд</p>
						<Button
							variant="primary"
							className="login"
							size="lg"
							data-toggle="modal"
							data-target="#modalAuth"
							onClick={() => {
								handleModalAuthActiveOpen();
								console.log(isModalAuthActive);
							}}
						>
							Попробовать
						</Button>
					</Col>
				</Row>
				<LoginModal
					store={store}
					showModal={isModalAuthActive}
					handleModalClose={handleModalAuthActiveClose}
					openRegClick={handleModalRegActiveOpen}
				/>
			</Container>
		</div>
	);
}

export default StartContent;
