import { observer } from "mobx-react";
import React, { useEffect, useState } from "react";
import { Col, Container, Row } from "react-bootstrap";
import ReactPaginate from "react-paginate";
import { useNavigate } from "react-router";
import "../../assets/css/style.css";
import store from "../../store/Store";
const HistoryOfRequests = observer(({ link }) => {
	const [currentPage, setCurrentPage] = useState(0);
	var totalPages = 0;
	const navigate = new useNavigate()
	const { getHistoryAction, links } = store; //получаем store
	const itemsPerPage = 3; // количество элементов на странице
	const handlePageChange = ({ selected }) => {
		setCurrentPage(selected);
	};
	useEffect(() => {
		store.getHistoryAction().then(() => {console.log("links: " + store.links);});
		// store.getHistoryAction()
		console.log("isAuthenticated: " + store.isAuthenticated);
	}, []);

	const renderData = () => {
		// Определение индексов начала и конца для текущей страницы
		const startIndex = currentPage * itemsPerPage;
		const endIndex = startIndex + itemsPerPage;
			totalPages = Math.ceil(store.links.length / itemsPerPage);
			// Отображение элементов для текущей страницы
			return (
				<div>
					{links.slice(startIndex, endIndex).map((link, index) => (
						<li key={index} className="list-group-item">
							<Container className="p-2">
							<Row className="d-flex justify-content-center align-items-center">

										<h5>Текст запроса: </h5><h3 className=" text-primary">"{link.text}"</h3>

								</Row>
								<Row>
									<Col md={10}>
										<div>
											{/*<h5>{link.title}</h5>*/}
											<h5 className=" text-secondary">
												Время запроса:{" "}
												{link.date_requested &&
													link.date_requested.slice(0, 10)}
												,{" "}
												{link.date_requested &&
													link.date_requested.slice(11, 19)}
											</h5>
										</div>
									</Col>
									<Col className="d-flex justify-content-end">
										<a
											href={link.url}
											target="_blank"
											rel="noopener noreferrer"
											className="btn btn-primary"
										>
											Перейти
										</a>
									</Col>
								</Row>
								
							</Container>
						</li>
					))}
				</div>
			);
		}




	return (
		<>
				{store.links ? <> <div className="container">
						<div>
							<ul className="list-group">
								{/* Отображение элементов списка для текущей страницы */}
								{renderData()}

								{/* Пагинация с использованием react-paginate */}
								<ReactPaginate
									pageCount={totalPages}
									previousLabel="назад"
									nextLabel="вперед"
									pageRangeDisplayed={5}
									marginPagesDisplayed={2}
									onPageChange={handlePageChange}
									containerClassName="pagination"
									activeClassName="active"
								/>
							</ul>
						</div>
					</div> </> : 

					<div className=" container">
					<p>История запросов пуста</p>
				</div>
}
		</>
		
	);
});

export default HistoryOfRequests;
