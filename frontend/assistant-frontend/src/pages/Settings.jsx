import React, { useState } from 'react';
import { Button, Container, Form, Row } from 'react-bootstrap';
import Header from '../components/Header';
import transition from '../transition';

function Settings({}) {
  const [text, setText] = useState("");
  const handleTextChange = (e) => {
    setText(e.target.value);
  };
  return (
    <div>
        <Header showBack={true}/>
        <Container>
            <Row>
                <h3 className='p-3'>Смена пароля</h3>
                <Form className='p-3'>
                    <Form.Control 
                      type="text"
                      placeholder="Введите новый пароль"
                      value={text}
                      onChange={handleTextChange}>
                      
                    </Form.Control>
                    <Button variant="outline-primary" type="submit" className='mt-3'>
                      Отправить
                  </Button>
                </Form>
            </Row>
        </Container>
    </div>
  )
}

export default transition( Settings)