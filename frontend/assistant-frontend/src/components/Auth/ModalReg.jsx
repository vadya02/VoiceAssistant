// import 'bootstrap/dist/css/bootstrap.min.css';
// import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import axios from 'axios';
import React, { useState } from 'react';
import { Button, Form, Modal } from 'react-bootstrap';

const ModalReg = (props) => {
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [checkPassword, setChechPassword] = useState(true);
  const [checkLogin, setCheckLogin] = useState(true);
  const handleSubmit = (event) => {
    // event.preventDefault(); // Предотвращаем стандартное поведение формы
    if (!passwordRegex.test(password)){
      setChechPassword(false)
      
    }
    else {
      setChechPassword(true)
      const userData = {
        email: email,
        username: username,
        password: password,
        re_password: confirmPassword
      };
      console.log(userData)
      const jsonString = JSON.stringify(userData);
      sendDataToServer(jsonString);
    }
    // Создайте объект с данными для отправки на сервер
    
    
  };

  const sendDataToServer = (data) => {

      axios({
        method: 'post',
        // url: 'https://chatbot.ext.lomger.tech/auth/users/',
        url: 'http://127.0.0.1:8000/auth/users/',
        // data: {
        //   email: data.email,
        //   username: data.username,
        //   password: data.password,
        //   re_password: data.confirmPassword
        // }
        data: data,
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      .then(response => {
        // Обработка успешного ответа
        setCheckLogin(true)
        console.log('Успешная регистрация:', response.data);
        alert('Регистрация прошла успешно')
        props.handleModalClose()
      })
      .catch((error) => {
        // Обработка ошибки
        console.log(error.data);
        console.log(error.response.data); // Данные ошибки от сервера
        console.log(error.response.status); // Код состояния
        console.log(error.response.headers);
        setUsername('')
        setPassword('')
        setConfirmPassword('')
        // console.log(response.data);
        console.error(error);
        if (error.response.data.username == 'A user with that username already exists.'){
          setCheckLogin(false)
        }

        
      });
  };

  
  const handleClick =()=>{
    props.openAuthClick();
    props.handleModalClose();
  }

  
    
  return (
    <div className="">
    <Modal show={props.showModal} onHide={props.handleModalClose} >
      <Modal.Header closeButton className='bg-dark text-light' style={{border: '1px solid gray'}}>
        <Modal.Title>Регистрация</Modal.Title>
      </Modal.Header>
      <Modal.Body className='bg-dark text-light' style={{border: '1px solid gray'}}>
        <Form onSubmit={handleSubmit}>
          {/* Форма регистрации */}
          <Form.Group controlId="formBasicEmail">
            <Form.Label>Email адрес</Form.Label>
            <Form.Control 
              type="email"
              placeholder="Введите email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </Form.Group>
          <Form.Group controlId="formBasicUsername">
            <Form.Label>Логин</Form.Label>
            <Form.Control
              type="text"
              placeholder="Введите логин"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </Form.Group>
          {!checkLogin && (
              <Form.Group style={{alignItems: 'center', display: 'flex', justifyContent: 'center', color: 'red'}}>
                <p>Пользователь с таким именем уже существует</p>
              </Form.Group>
            )}
          <Form.Group controlId="formBasicPassword">
            <Form.Label>Пароль</Form.Label>
            <Form.Control 
              type="password"
              placeholder="Введите пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Form.Group>
          {!checkPassword && (
              <Form.Group style={{alignItems: 'center', display: 'flex', justifyContent: 'center', color: 'red'}}>
                <p>Пароль должен состоять из букв и цифр, а также быть не короче 8 символов</p>
              </Form.Group>
            )}
          <Form.Group controlId="formBasicPassword">
            <Form.Label>Подтвердите пароль</Form.Label>
            <Form.Control 
              type="password"
              placeholder="Введите пароль"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </Form.Group>
          {!checkPassword && (
              <Form.Group style={{alignItems: 'center', display: 'flex', justifyContent: 'center', color: 'red'}}>
                <p>Пароль должен состоять из букв и цифр, а также быть не короче 8 символов</p>
              </Form.Group>
            )}
          <Form.Group style={{alignItems: 'center', display: 'flex', justifyContent: 'center', padding: '10px'}}>
                <Button variant="primary" type="submit" style={{alignItems: 'center', display: 'flex', justifyContent: 'center', width: '200px'}}  >
                    Зарегистрироваться
                </Button>
            </Form.Group>
          <Form.Group style={{alignItems: 'center', display: 'flex', justifyContent: 'center', margin: '5px'}}>
                <Form.Label>Уже зарегистрированы?</Form.Label>
                <Form.Label style={{color: '#0D6EFD', cursor: 'pointer'}} onClick={handleClick}>Войти</Form.Label>
            </Form.Group>
          
        </Form>
      </Modal.Body>
    </Modal>
    </div>

  );
}

export default ModalReg;