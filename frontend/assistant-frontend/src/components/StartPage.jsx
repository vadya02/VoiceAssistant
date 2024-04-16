import axios from "axios";
import { observer } from "mobx-react";
import React, { useEffect } from 'react';
import { useNavigate } from "react-router";
import Store from "../store/Store";
import Header from './Header';
import StartContent from './StartContent';

const StartPage = observer(({}) => {
    const navigate = new useNavigate()
    useEffect(() => {
        // При загрузке компонента
        const authToken = localStorage.getItem('authToken');

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
                    navigate('/MainPage')
                    console.log(process.env.REACT_URL)
                })
                .catch(error => {
                    console.log('Ошибка проверки авторизации:', error);
                    Store.setIsAuthenticated(false)
                });
        }
    }, [navigate]);

  return (
    <div style={{height: '90vh'}}>
        <Header showBack={false}/>
        <StartContent/>
        {console.log(process.env.REACT_APP_URL)}
        {/* <Test/> */}
    </div>
  )
})

export default StartPage