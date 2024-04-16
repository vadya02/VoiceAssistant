import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';
import { observer } from "mobx-react";
import React, { useEffect, useState } from 'react';
import { Button, Dropdown, Nav, Navbar } from "react-bootstrap";
import { useNavigate } from 'react-router';
import Logo from '../img/Logo.png';
import { default as Store, default as store } from "../store/Store";
import LoginModal from "./Auth/LoginModal";
import ModalReg from "./Auth/ModalReg";

const Header = observer(({showBack}) => {
  // const { userStore } = store(); // Подставьте ваше хранилище MobX
  const authToken = localStorage.getItem('authToken');
  const navigate = useNavigate()
  const [isModalAuthActive, setIsModalAuthActive] = useState(false)
  const [isModalRegActive, setIsModalRegActive] = useState(false)
  const [nickname, setNickname] = useState('')
  function handleModalAuthActiveOpen () {
      setIsModalAuthActive(true)
  } 
  function handleModalAuthActiveClose (){
      setIsModalAuthActive(false)
  } 
  function handleModalRegActiveOpen () {
      setIsModalRegActive(true)
  } 
  function handleModalRegActiveClose (){
      setIsModalRegActive(false)
  }
  function handleQuit(){
    store.setIsAuthenticated(false)
      localStorage.removeItem('authToken');
    navigate('/StartPage')
  }
  const getUserData = () => {
    axios({
      method: 'GET',
      url: `${process.env.REACT_APP_URL_BACKEND}get_user_data/`, // Замените на ваш URL для проверки авторизации
      headers: {
          Authorization: `Token ${authToken}`,
      },
  })
      .then((response) => {
        console.log(response.data.username)
        setNickname(response.data.username)
      })
      .catch(error => {

      });
  }
    useEffect(() => {
        // При загрузке компонента
        getUserData()

        if (authToken) {
            // Если есть токен, проверяем его на сервере
            axios({
                method: 'GET',
                url: `${process.env.REACT_APP_URL_BACKEND}auth/users/me/`, // Замените на ваш URL для проверки авторизации
                headers: {
                    Authorization: `Token ${authToken}`,
                },
            })
                .then(() => {
                    //   Store.login(); // Если токен валиден, устанавливаем состояние авторизации
                    Store.setIsAuthenticated(true)
                })
                .catch(error => {
                    console.log('Ошибка проверки авторизации:', error);
                    Store.setIsAuthenticated(false)
                });
        }
    }, []);
  return (
      <div>
        <header style={{backgroundColor: 'black'}}>
      
        <Navbar className='p-3'>
          
            <Navbar.Brand href="#">
              <img src={Logo}/>
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            {/* <div className="d-flex justify-content-end"> */}
            <Navbar.Collapse id="navbarScroll">

            <Nav
              className="me-auto my-2 my-lg-0"
              style={{ maxHeight: '100px' }}
              navbarScroll
            >
                {/* {store.isAuthenticated ? (
                  <Button variant="outline-primary">Личный кабинет</Button>
                ) : (
                  <>
                    <Button variant="outline-primary" className='m-100' onClick={()=>{handleModalAuthActiveOpen();}}>
                      Вход
                    </Button>
                    <Button variant="outline-primary" onClick={()=>{handleModalRegActiveOpen()}}>
                      Регистрация
                    </Button>
                  </>
                )} */}
              </Nav>
              <Nav>
                {(store.isAuthenticated && !showBack) && (
                  <div className='container d-flex bd-highlight'>
                    <h5 className='p-2 justify-content-center aligh-items-center' style={{color: 'white'}}>{nickname}</h5>
                    <Dropdown
                      
                      align={{ lg: 'end' }}
                      title="Left-aligned but right aligned when large screen"
                      id="dropdown-menu-align-responsive-1"
                    >
                      <Dropdown.Toggle variant="outline-secondary" id="dropdown-basic">
                        
                      </Dropdown.Toggle>

                      <Dropdown.Menu>
                        <Dropdown.Item onClick={()=>navigate('/Settings')}>
                          
                          Настройки
                        </Dropdown.Item>
                        <Dropdown.Item href="#/action-2" onClick={() => handleQuit()}>
                          Выход
                        </Dropdown.Item>
                      </Dropdown.Menu>
                    </Dropdown>
                    {/* <Button variant="outline-primary" className='me-2'>Личный кабинет</Button>
                    <Button variant="outline-danger">Выход</Button> */}
                  </div>
                ) }
                 {(!store.isAuthenticated) && (
                  <>
                    <Button variant="secondary" className='me-2' onClick={()=>{handleModalAuthActiveOpen();}}>
                      Вход
                    </Button>
                    <Button variant="secondary" onClick={()=>{handleModalRegActiveOpen()}}>
                      Регистрация
                    </Button>
                  </>
                )}
                {(store.isAuthenticated && showBack) && (
                  <>
                    <Button variant="secondary" className='me-2' onClick={()=>{navigate('/MainPage')}}>
                      На главную
                    </Button>
                    
                  </>
                )}
              </Nav>
            </Navbar.Collapse>
            {/* </div> */}
            <LoginModal store={store} showModal = {isModalAuthActive} handleModalClose = {handleModalAuthActiveClose} openRegClick={handleModalRegActiveOpen}/>
            <ModalReg store={store} showModal = {isModalRegActive} handleModalClose = {handleModalRegActiveClose} openAuthClick={handleModalAuthActiveOpen}/>
          
        </Navbar>
        </header>
        </div>
  );
});

export default Header;