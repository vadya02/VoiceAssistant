import { observer } from "mobx-react";
import React, { useEffect, useState } from "react";
import { Col, Container, Row } from "react-bootstrap";
import ReactPaginate from "react-paginate";
import "../../assets/css/style.css";
import store from "../../store/Store";
const HistoryOfRequests = observer(({ link }) => {
	const [currentPage, setCurrentPage] = useState(0);
	const {getHistoryAction, links} = store //получаем store
	const itemsPerPage = 5; // количество элементов на странице
	const handlePageChange = ({ selected }) => {
		setCurrentPage(selected);
	};
	useEffect(() => {
		getHistoryAction()
	})

	const renderData = () => {
		// Определение индексов начала и конца для текущей страницы
		const startIndex = currentPage * itemsPerPage;
		const endIndex = startIndex + itemsPerPage;

		// Отображение элементов для текущей страницы
		return links.slice(startIndex, endIndex).map((link, index) => (
			<li key={index} className="list-group-item">
				<Container>
					<Row>
						<Col md={10}>
							<div>
								{/*<h5>{link.title}</h5>*/}
								<h5>
									Время запроса:{" "}
									{link.date_requested && link.date_requested.slice(0, 10)},{" "}
									{link.date_requested && link.date_requested.slice(11, 19)}
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
					<Row>
						<div className="row">
							<h5>Текст запроса: "{link.text}"</h5>
						</div>
					</Row>
				</Container>
			</li>
		));
	};

	const totalPages = Math.ceil(links.length / itemsPerPage);

	return (
		<div className="container">
			{/* <ul className="list-group">
				{links.map((link, index) => (
					<li key={index} className="list-group-item">
						<Container>
							<Row>
								<Col md={10}>
									<div>
										<h5>
											Время запроса:{" "}
											{link.date_requested && link.date_requested.slice(0, 10)},{" "}
											{link.date_requested && link.date_requested.slice(11, 19)}
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
							<Row>
								<div className="row">
									<h5>Текст запроса: "{link.text}"</h5>
								</div>
							</Row>
						</Container>
					</li>
				))}
			</ul> */}
			<div>
				<ul className="list-group">
					{/* Отображение элементов списка для текущей страницы */}
					{renderData()}

					{/* Пагинация с использованием react-paginate */}
					<ReactPaginate
						pageCount={totalPages}
						pageRangeDisplayed={5}
						marginPagesDisplayed={2}
						onPageChange={handlePageChange}
						containerClassName="pagination"
						activeClassName="active"
					/>
				</ul>
			</div>
		</div>
	);
});

export default HistoryOfRequests;
