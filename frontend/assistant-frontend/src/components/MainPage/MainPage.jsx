import '@mohayonao/web-audio-api-shim'
import axios from 'axios'
import React, { useEffect, useRef, useState } from 'react'
import { Button, Container, Form, FormControl, Row } from 'react-bootstrap'
import { useNavigate } from 'react-router'
import Header from '../Header'

// import PcmUtil from 'pcm-util';
import { observer } from "mobx-react"
import HistoryOfRequests from "../Dashboard/HistoryOfRequests"
import VoiceRecorderWAV from "./VoiceRecorderWAV"

// const appId = '<INSERT_SPEECHLY_APP_ID_HERE>';
// const SpeechlySpeechRecognition = createSpeechlySpeechRecognition(appId);
// SpeechRecognition.applyPolyfill(SpeechlySpeechRecognition);
var options = {
    audioBitsPerSecond : 48000,
}

const MainPage = observer((props) => {
    axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('authToken')}`;
    const [recording, setRecording] = useState(false);
    const audioRef = useRef();
    const audioChunks = useRef([]);
    const navigate = useNavigate()
    const [text, setText] = useState("");
    const [links, setLinks] = useState([]);
    const getHistory = () => {
        axios.get('http://127.0.0.1:8000/get_history_of_requests/')
        .then(response => {
            setLinks(response.data);
            console.log('история запросов: ' + response.data)
            console.log(links)
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }
    useEffect(() => {
        // Загрузка данных с сервера (предположим, что сервер возвращает массив объектов)
        getHistory()
    }, []); // Пустой массив зависимостей, чтобы useEffect сработал только один раз при монтировании компонента

    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorder = useRef(null);
    const chunks = useRef([]);

    
  
    const handleTextChange = (e) => {
      setText(e.target.value);
    };



    let audioContext = new window.AudioContext();
    
  
    const startRecording = () => {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
          mediaRecorder.current = new MediaRecorder(stream, options);
          
          mediaRecorder.current.ondataavailable = (e) => {
            if (e.data.size > 0) {
              chunks.current.push(e.data);
            }
          };
          
          mediaRecorder.current.onstop = () => {
            const recordedBlob = new Blob(chunks.current, { type: 'audio/wav' }); // Замените на поддерживаемый формат
            // const pcmWavBlob = PcmUtil.encodeWav(recordedBlob, { numChannels: 1, sampleRate: 44100, float32: false });
            const audioElement = new Audio();
            console.log(recordedBlob)
            uploadAudioFile(recordedBlob)
            // Здесь вы можете использовать recordedBlob, например, отправить на сервер
            chunks.current = [];
          };
  
          mediaRecorder.current.start();
          setIsRecording(true);
          
        })
        .catch((error) => {
          console.error('Error accessing microphone:', error);
          setIsRecording(false);
        });
    };
    const stopRecording = () => {
      if (mediaRecorder.current) {
        mediaRecorder.current.stop();      
        setIsRecording(false);
      }
    };
    
    const uploadAudioFile = (audioBlob) => {
      const formData = new FormData();
      formData.append('audio_file', audioBlob, 'voiceRecording.wav'); // Имя 'audio' - это ключ, используемый на сервере
      // Здесь вы можете добавить другие данные, если необходимо
      console.log(formData)
      axios.post('http://127.0.0.1:8000/upload_audio_file_mp3/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
        .then((response) => {
          console.log('Audio file uploaded successfully:', response.data);
            window.open(response.data.url, '_blank');
        })
        .catch((error) => {
          console.error('Error uploading audio file:', error);
        });
    };
    const uploadTextRequest = (request) => {

      console.log(request)
       // Имя 'audio' - это ключ, используемый на сервере
      // Здесь вы можете добавить другие данные, если необходимо
      // navigate('/Dashboard')
      axios.post('http://127.0.0.1:8000/upload_audio_text/', {
          headers: {
              'Authorization': `Token ${localStorage.getItem('authToken')}`
          },
          textRequest: request
      })
        .then((response) => {
          getHistory()
          console.log('Audio file uploaded successfully:', response.data);
            window.open(response.data.url, '_blank');
        })
        .catch((error) => {
          console.error('Error uploading audio file:', error);
        });
    };
    





  return (
    <div >
        <Header/>
        <Container>
            
            <Row style={{backgroundColor: '#EFEFEF', margin: '20px', borderRadius: '20px'}} className="d-flex justify-content-center align-items-center pt-3">
                <h2 className='text-center'>Введите голосовую команду (сделать анимацию частоты звука при вводе команды)</h2>
                <VoiceRecorderWAV getHistory={getHistory}/>
            </Row>
            <Row style={{backgroundColor: '#EFEFEF', margin: '20px', borderRadius: '20px'}} className="d-flex justify-content-center align-items-center">
                <h3 className='text-center m-2'>Введите текстовую команду</h3>
                <Form className="d-flex justify-content-center align-items-center m-2">
                  <FormControl
                      type="text"
                      placeholder={"Введите текстовый запрос"}
                      value={text}
                      onChange={handleTextChange}
                      className="m-2"
                  />
                  <Button variant="outline-primary" onClick={() => uploadTextRequest(text)}>
                      Отправить
                  </Button>
                </Form>
            </Row>
            <Row className="d-flex justify-content-center align-items-center">
                <h5 className='text-center'>История запросов (изменить формат элементов, поправить время)</h5>
                <HistoryOfRequests links={links}/>
                {/*<HistoryOfDashboards/>*/}
            </Row>
            {/*<VoiceRecorder/>*/}
            {/*<AudioRecorder/>*/}

            {/*<RecorderJSDemo/>*/}
            {/*<VoiceRecorderJSX/>*/}
        </Container>
        
    </div>
  )
})

export default MainPage