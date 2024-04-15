import React from 'react'
import { useState, useEffect } from 'react'
import { Button, Card, CardBody, Row, Col, Container } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import store, { storeType } from '../../store/Store'
import axios from 'axios'
import ImageDashboard from '../../img/dashboard.png'
import Header from '../Header'
import Image from 'react-bootstrap/Image'
// import ImageDashboard from '../../img/dashboard.png'


function Dashboard({}) {
  useEffect(() => {
    // console.log("Текущая марка: " + CarDescriptionStore.Marka)
    // console.log("Текущая модель: " + CarDescriptionStore.Model)
    // handleMarkaGet();
    // handleCarDescriptionList()
    // handleModelList(CarDescriptionStore.Model)
    // storedToken = localStorage.getItem('authToken');
    // if (storedToken) {
    //   Store.login();
    // }
    // setShowCalculator(Store.isAuthenticated)
  }, []);
  const [dashboardHistoryList, setDashboardHistoryList] = useState([]);
  const [dashboard, setDashboard] = useState([]);
  const userDataArray = [
    { id: 1, name: 'John', email: 'john@example.com', main_image: 'картинка', name_of_dashboard: 'Дашборд от 13.11.23' },
    { id: 2, name: 'Jane', email: 'john@example.com', main_image: 'картинка', name_of_dashboard: 'Дашборд от 13.11.23' },
    // Добавьте другие объекты с данными
  ];
  const handleCarDescriptionList = async () => {
    await axios.get('http://127.0.0.1:8000/car_descriptions_all', { 
      method: 'GET',
      // params: {
      //   Nazvanie_modeli: model
      // },
      headers: {
          "Content-type": "application/json; charset=UTF-8"
      }

    })
    .then(response => {
      console.log(response.data)
      setDashboardHistoryList(response.data)
    })
    .catch(error => {
      // Обработка ошибки
      console.error(error);
    });
  }
  return (
    <div>
      <Header store={store} showBack={true}/>
      <Container>
        
        <Row className="d-flex justify-content-center align-items-center p-5">
            <h3 className='text-center'>Дашборд по запросу: {dashboard}</h3>

        </Row>
        <Row>
            <Image src={ImageDashboard} fluid className="rounded mx-auto"/>
        </Row>
      </Container>
        
    </div>
  )
}

export default Dashboard