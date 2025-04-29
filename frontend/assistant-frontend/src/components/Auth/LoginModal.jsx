import axios from "axios";
import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { useNavigate } from "react-router";
import store from "../../store/Store";
import LoadingOverlayLogin from "./LoadingOverlayLogin";
const LoginModal = (props) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [checkLogin, setcheckLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const navigate = useNavigate();
  const [show, setShow] = useState(false);
  const handleClick = () => {
    setcheckLogin(true);
    props.openRegClick();
    props.handleModalClose();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      username: username,
      password: password,
    };

    const UserData = JSON.stringify(data);
    console.log(UserData);
    // setLoading(true);
    // new Promise((resolve) => setTimeout(resolve, 500))
    axios({
      method: "post",
      url: `${process.env.REACT_APP_URL_BACKEND}auth/token/login/`,
      data: UserData,
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        // Обработка успешного входа
        setcheckLogin(true);
        console.log("Успешный вход:", response.data);
        localStorage.setItem("authToken", response.data.auth_token);
        store.setIsAuthenticated(true);
        navigate("/MainPage");
      })
      .catch((error) => {
        console.log("ошибка:", error.response.data);
        // Обработка ошибки
        setLoading(false);
        setcheckLogin(false);
        console.error("Ошибка входа:", error);
      });
  };
  return (
    <>
      <Modal
        show={props.showModal}
        onHide={props.handleModalClose}
        size="md"
        aria-labelledby="contained-modal-title-vcenter"
        centered
        className=""
      >
        <Modal.Body className="bg-dark text-light rounded-5">
          <h1 className="text-center mt-3 fw-normal fs-2 mb-2 text-uppercase">Вход</h1>
          <Form onSubmit={handleSubmit} className="m-3">
            <Form.Group controlId="formBasicUserName" className="m-2">
              <Form.Label >Логин</Form.Label>
              <Form.Control
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Введите логин"
                className="p-3"
              />
            </Form.Group>
            <Form.Group
              controlId="formBasicPassword" className="m-2"
            >
              <Form.Label >Пароль</Form.Label>
              <Form.Control
                type="password"
                value={password}
                className="p-3"
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Введите пароль"
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
                <p>Неверный пароль или логин</p>
              </Form.Group>
            )}

            <Form.Group
              style={{
                alignItems: "center",
                display: "flex",
                justifyContent: "center",
              }}
            >
              <Button
                variant="primary"
                type="submit"
                className="m-3 px-5"
                size="lg "
                onClick={() => {
                  setLoading(true);
                  // props.handleModalClose()
                  // Имитация задержки при авторизации
                  setTimeout(() => {
                    // Успешная авторизация
										setLoading(false);
										// navigate('/MainPage')
										// store.setIsAuthenticated(true)
									}, 1000);
								}}
							>
								Войти
							</Button>
						</Form.Group>
					</Form>
				</Modal.Body>
			</Modal>
			{loading && <LoadingOverlayLogin show={loading} />}
		</>
	);
}

export default LoginModal;
