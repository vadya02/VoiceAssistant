import React, { useState } from 'react'
import { Container, Row } from 'react-bootstrap'
import Image from 'react-bootstrap/Image'
import ImageDashboard from '../../img/dashboard.png'
import store from '../../store/Store'
import Header from '../Header'
// import ImageDashboard from '../../img/dashboard.png'


function Dashboard({}) {

  const [dashboard, setDashboard] = useState([]);
  
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