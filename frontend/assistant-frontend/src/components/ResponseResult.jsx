import { observer } from "mobx-react";
import React from "react";
import { Container, Modal, Row, Table } from "react-bootstrap";
import store from "../store/Store";
const ResponseResult = observer((props) => {
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
					<Container className="p-3">
						<h2 className=" text-center mb-3">Результат запроса</h2>
						<Row className=" bg-black bg-opacity-50 p-3 rounded-3">
						{store.checkResult && (
							<Table className=" bg-dark bg-black" striped>
								<thead className=" bg-dark bg-black">
									<tr className=" bg-dark bg-black">
										<th className=" bg-dark bg-black text-light">Название фильтра</th>
										<th className=" bg-dark bg-black text-light">Значение фильтра</th>
									</tr>
								</thead>
								<tbody>
									<tr>
									<th>Команда</th>
									<th>{store.filtersResponse.command}</th>
									</tr>
									<tr>
									<th>Дашборд</th>
									<th>{store.filtersResponse.dashboards.value}</th>
									</tr>
									

										{store.filtersResponse.filters.map((item, index) => (
											<>
											<tr>
											<th key={index}>{item.initial_name}</th>
											<th key={index}>{item.initial_value}</th>
											</tr>
											</>
											
										))}
									
									
								</tbody>
							</Table>)}
							{/* {store.checkResult && (
								<Row className="align-items-center justify-content-center">
									<h5 className=" p-2 bg-dark rounded-3">Команда: {store.filtersResponse.command}</h5>
									<h5 className=" p-2 bg-dark rounded-3">Дашборд: {store.filtersResponse.dashboards.value}</h5>
									{store.filtersResponse.filters.map((item, index) => (
										<>
											<h5 key={index} className=" p-2 bg-dark rounded-3 align-items-center justify-content-center">
												{item.initial_name}: {item.initial_value.map((item, index) => (<p key={index}>{item}</p>))}
											</h5>
										</>
									))}
									
									
								</Row>
							)} */}
						</Row>

						<Row className=" align-items-center justify-content-center flex-column p-3">
							<a
								href={store.response.url}
								target="_blank"
								rel="noopener noreferrer"
								className="btn btn-success w-50"
							>
								Посмотреть результат в Apache Superset
							</a>
						</Row>
					</Container>
				</Modal.Body>
			</Modal>
		</>
	);
});

export default ResponseResult;
