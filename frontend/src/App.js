import {useState} from 'react';
import './App.css';
import 'antd/dist/antd.css';
import Row from 'antd/lib/row';
import Col from 'antd/lib/col';
import Button from 'antd/lib/button';
import Select from 'antd/lib/select';

const { Option } = Select;


function App() {

  const hostname = "localhost";
  const port = "8000"
  const urlPort = `http://${hostname}:${port}/port`;
  const urlConnect = `http://${hostname}:${port}/connect`;
  const urlDisconnect = `http://${hostname}:${port}/disconnect`;

  const [ports, setPorts] = useState([]);
  const [serPort, setSerPort] = useState();

  const apiGet = (
    url,
    processor=v=>{console.log(v); return v},
    errorHandler=console.error,
  ) => {
    const d = new Date();
    fetch(url)
      .then(res => res.json())
      .then(processor)
      .then((res) => console.log(d.toISOString(), 'Get data from API:', res))
      .catch(errorHandler);
  };

  const apiPost = (url, data) => {
    const d = new Date();
    console.log(d.toISOString(), 'Post data to API:', data);
    fetch(url, {
      method: "POST",
      headers: {
        'Accept': 'application/json, text/plain',
        'Content-Type': 'application/json; charset=UTF-8',
        // 'X-CSRFToken': csrftoken
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(res => console.log(d.toISOString(), 'Post response from API:', res))
      .catch(console.error);
  };

  const getPortsProcessor = v => {
    // console.log(v);
    setPorts(v);
    return v;
  };

  const getPorts = () => {
    apiGet(urlPort, getPortsProcessor);
  };

  const selectPort = v => {
    // console.log(v);
    setSerPort(v);
  };

  const comfirmPort = () => {
    apiPost(urlPort, {'port': serPort});
  };

  const connect = () => {
    apiGet(urlConnect);
  };
  
  const disconnect = () => {
    apiGet(urlDisconnect);
  };

  return (
    <div className="App">
      <Row style={{ marginTop: 20}}>
        <Col style={{ margin: 10}} span={24}>
          <Row style={{ margin: 10}}>
            <Button style={{ marginRight: 10}} onClick={getPorts}>Get Ports</Button>
            <Button style={{ marginLeft: 10}} onClick={comfirmPort}>Comfirm</Button>
          </Row>
          <Row style={{ margin: 10}}>
            <Select
              style={{ width: 300 }}
              placeholder='Port'
              onSelect={selectPort}
            >
              { ports.map((v, i) => <Option key={i} value={v}>{v}</Option>)}
            </Select>
          </Row>
          <Row style={{ margin: 10}}>
            <Button style={{ marginRight: 10}} onClick={connect}>Connect</Button>
            <Button style={{ marginLeft: 10}} onClick={disconnect}>Disonnect</Button>
          </Row>
        </Col>
      </Row>
    </div>
  );
}

export default App;
