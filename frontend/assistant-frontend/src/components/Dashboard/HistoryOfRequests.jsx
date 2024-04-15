import { observer } from "mobx-react";
import React, { useState } from "react";
import { Col, Container, Row } from "react-bootstrap";
import ReactPaginate from "react-paginate";
import '../../css/style.css';
const HistoryOfRequests = observer(({ links }) => {
	const [currentPage, setCurrentPage] = useState(0);
	const itemsPerPage = 5; // количество элементов на странице
	const handlePageChange = ({ selected }) => {
		setCurrentPage(selected);
	};
	const mockData = [
		{
			title: "Запрос",
			url: "http://213.171.10.37:8088/superset/dashboard/12/?native_filters_key=jq9pf2aXz9sgIwMI4e93RLk20IGHu5DI5-Q30RvvwuMqUI4aa00PjdbJvzOkwzNv",
			date: "2023-11-27",
		},
	];

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
