// LoadingOverlay.tsx
import React from "react";
import { Container, Row } from "react-bootstrap";
import "./Auth.css";
const LoadingOverlayLogin = ({ show }) => {
	return (
		<div className={`overlay ${show ? "active" : ""}`}>
			<div className="overlay-content">
				<div className="text-center">

					<Container className="bg-light p-5 px-5 rounded-3">
						<Row className="d-flex justify-content-center align-items-center">
							<h3>Загрузка...</h3>
						</Row>
						<Row className="d-flex justify-content-center align-items-center">
							<div className="spinner-border" role="status">
								{/* <span className="visually-hidden">Loading...</span> */}
							</div>
						</Row>
						<Row className="d-flex justify-content-center align-items-center pt-2">

						</Row>
					</Container>
				</div>
			</div>
		</div>
	);

	// <Modal show={show} keyboard={false} centered >
	//   <Spinner animation="border"></Spinner>
	// </Modal>
};

export default LoadingOverlayLogin;
