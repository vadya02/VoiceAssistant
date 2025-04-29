import React from 'react'
import { Container, Row } from 'react-bootstrap'
import Header from '../components/Header'
import HistoryOfRequests from '../modules/History/HistoryOfRequests'
import store from '../store/Store'
const History = () => {
  return (
    <div>
      <Header showBack={true}/>
      <Container>
      <Row
					style={{
						backgroundColor: "#EFEFEF",
						margin: "20px",
						borderRadius: "20px",
					}}
					className="d-flex justify-content-center align-items-center"
				>
					<h5 className="text-center mt-3">История запросов</h5>
					{store.links ? (
						<HistoryOfRequests links={store.links} />
					) : (
						<div className="d-flex justify-content-center align-items-center">
							<p>Нет ранее выполненных запросов</p>
						</div>
					)}
				</Row>
      </Container>
    </div>
  )
}

export default History
