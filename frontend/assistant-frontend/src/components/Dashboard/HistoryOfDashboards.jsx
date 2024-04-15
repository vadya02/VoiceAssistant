import React from 'react'
import { useState, useEffect } from 'react'
import { Button, Card, CardBody, Row, Col, Pagination } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import axios from 'axios'
import ImageDashboard from '../../img/dashboard.png'



function HistoryOfDashboards({}) {
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
  let active = 2;
  let items = [];
  for (let number = 1; number <= 5; number++) {
    items.push(
      <Pagination.Item key={number} active={number === active}>
        {number}
      </Pagination.Item>,
    );
  }
  return (
    <div>
      <Row xs={1} md={2} className="g-4">
            {userDataArray&&
              userDataArray.map((car) => (
              // <Card key={car.id} className="bg-black text-light " style={{borderColor: 'gray'}}>
              //   <Card.Body>
              //     <Image src={car.main_image} fluid className="rounded mx-auto"/>
              //   </Card.Body>
              // </Card>
              <Col key={car.id} style={{padding: '60px'}}>
                <Card className='bg-dark text-light'>
                  
                  <Card.Body>
                    
                    <Card.Img variant="top" src={ImageDashboard}/>
                    <Card.Title>{car.name_of_dashboard}</Card.Title>
                    <Row>
                      <Col>
                        <Button onClick={()=>{
                          // store.updateMarka(CarDescriptionList[car.id-1].marka_name) 
                          // CalculatorStore.updateModel(CarDescriptionList[car.id-1].model_name) 
                          // CarDescriptionStore.updateSalonImage(CarDescriptionList[car.id-1].salon_image)  
                          // CarDescriptionStore.updateCarDescription(CarDescriptionList[car.id-1].description) 
                          }   
                        }>
                          <Link style={{color: 'white', textDecoration: "none"}} to='/Dashboard' id='navbarNav' className='nav-item'>Подробнее</Link>
                        </Button>
                      </Col>
                      <Col>
                      <Button variant='outline-secondary' onClick={()=>{
                          
                        }   
                      }>
                        <Link style={{color: 'white', textDecoration: "none"}} to='/Dashboard' id='navbarNav' className='nav-item'>Повторить</Link>
                        
                      </Button>
                      <Button variant='outline-danger' onClick={()=>{
                        
                          }   
                        }>
                      <Link style={{color: 'white', textDecoration: "none"}} to='/Dashboard' id='navbarNav' className='nav-item'>Удалить</Link>
                      
                      </Button>
                      </Col>
                    </Row>
                      
                      
                    </Card.Body>
                </Card>
              </Col>
            ))}
            
          </Row>
          <Row>
            <Pagination className="d-flex justify-content-center align-items-center">{items}</Pagination>
          </Row>
    </div>
  )
}

export default HistoryOfDashboards