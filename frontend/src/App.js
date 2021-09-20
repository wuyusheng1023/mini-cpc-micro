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

  const [ports, setPorts] = useState([]);

  const apiGet = (
    url,
    processor=f=>f,
    errorHandler=console.error
  ) => {
    const d = new Date();
    fetch(url)
      .then(res => res.json())
      .then(processor)
      .then((res) => console.log(d.toISOString(), 'Get data from API:', res))
      .catch(errorHandler);
  };

  const apiPost = (data, url) => {
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
      .then((res) => console.log(d.toISOString(), 'Post response from API:', res))
      .catch(console.error);
  };

  const getPortsProcessor = v => {
    console.log(v);
    setPorts(v);
    return v;
  };

  const getPorts = () => {
    apiGet(urlPort, getPortsProcessor);
  };

  const onSelectPort = v => {
    console.log(v);
  };

  return (
    <div className="App">
      <Row style={{ marginTop: 20}}>
        <Col style={{ margin: 10}} span={24}>
          <Row style={{ margin: 10}}>
            <Button onClick={getPorts}>
              Get Ports
            </Button>
          </Row>
          <Row style={{ margin: 10}}>
            <Select
              style={{ width: 300 }}
              placeholder='Port'
              onSelect={onSelectPort}
            >
              { ports.map((v, i) => <Option key={i} value={v}>{v}</Option>)}
            </Select>
          </Row>
        </Col>
      </Row>
    </div>
  );
}

export default App;
