import axios from "axios";
import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { useNavigate } from "react-router";
import store from "../../store/Store";
import LoadingOverlay from "./LoadingOverlay";

const LoginModal = (props) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [checkLogin, setcheckLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const navigate = useNavigate()
  const [show, setShow] = useState(false);
  const handleClick =()=>{
    setcheckLogin(true)
    props.openRegClick();
    props.handleModalClose();
  }

  

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      username: username,
      password: password,
    };
    console.log(data)
    const UserData = JSON.stringify(data);
    // setLoading(true);
    // new Promise((resolve) => setTimeout(resolve, 500))
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/auth/token/login/`,
      data: UserData,
      headers: {
        'Content-Type': 'application/json',
      },
    })
      
      .then(response => {
        
        // Обработка успешного входа
        setcheckLogin(true)
        console.log('Успешный вход:', response.data);
        localStorage.setItem('authToken', response.data.auth_token);
        store.setIsAuthenticated(true)
        navigate('/MainPage')
        // handleModalClose();
        // return redirect('/about')
      })
      .catch(error => {
        // Обработка ошибки
        setLoading(false)
        setcheckLogin(false)
        console.error('Ошибка входа:', error);
      });
    };
  return (
    <>
      <div className='bg-black text-light'>
      <Modal show={props.showModal} onHide={props.handleModalClose}>
        <Modal.Header className='bg-dark text-light' closeButton style={{border: '1px solid gray'}}>
          <Modal.Title>Авторизация и регистрация</Modal.Title>
        </Modal.Header>
        <Modal.Body className='bg-dark text-light' style={{border: '1px solid gray'}}>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formBasicUserName">
              <Form.Label>Логин</Form.Label>
              <Form.Control type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder='Введите логин'/>
              <Form.Group controlId="formBasicPassword" style={{paddingBottom: '10px'}}>
                <Form.Label>Пароль</Form.Label>
                <Form.Control type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder='Введите пароль'/>
              </Form.Group>
              {/* <Form.Text className="text-muted">
                Мы никогда не передадим вашу электронную почту кому-либо еще.
              </Form.Text> */}
            </Form.Group>
            {!checkLogin && (
              <Form.Group style={{alignItems: 'center', display: 'flex', justifyContent: 'center', color: 'red'}}>
                <p>Неверный пароль или логин</p>
              </Form.Group>
            )}
            

            
            <Form.Group style={{alignItems: 'center', display: 'flex', justifyContent: 'center'}}>
                <Button variant="primary" type="submit" 
                  style={{alignItems: 'center', display: 'flex', justifyContent: 'center', width: '200px', padding:'5px'}}
                  onClick={()=> 
                    {
                      setLoading(true);
                      // props.handleModalClose()
                      // Имитация задержки при авторизации
                      setTimeout(() => {
                        // Успешная авторизация
                        
                        setLoading(false);
                        // navigate('/MainPage')
                        // store.setIsAuthenticated(true)
                      }, 1000);
                      
                      
                    }
                  } >
                    Войти
                </Button>
            </Form.Group>
            <Form.Group style={{alignItems: 'center', display: 'flex', justifyContent: 'center', margin: '5px'}}>
                <Form.Label>Еще не зарегистрированы?</Form.Label>
                <Form.Label style={{color: '#0D6EFD', cursor: 'pointer'}} onClick={handleClick}>Зарегистрироваться</Form.Label>
            </Form.Group>
            
          </Form>
        </Modal.Body>
      </Modal>
      {loading && (<LoadingOverlay show={loading} />)}
      
      </div>
    </>
  );
};

export default LoginModal;