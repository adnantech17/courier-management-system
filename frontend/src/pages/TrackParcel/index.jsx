import ProForm, { ProFormSelect, ProFormText } from '@ant-design/pro-form';
import { PageContainer } from '@ant-design/pro-layout';
import { Row, Col, message, Table, Button, Steps } from 'antd';
import { useState } from 'react';
import { trackParcel } from './service';

import styles from './index.less';

const { Step } = Steps;

const EntryForm = () => {
  const [form] = ProForm.useForm();
  const [parcels, setParcels] = useState([]);
  const [tracking, setTracking] = useState([]);

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }).format(new Date(dateString));
  };

  const handleSubmit = async (data, clear) => {
    try {
      const params = {};
      params[data.type] = data.value;
      const resp = await trackParcel(params);
      if (!resp.success) throw resp.data;
      if (clear) {
        setTracking([]);
        setParcels([]);
      }
      if (resp.type == 'parcels') setParcels(resp.data);
      else setTracking(resp.data);
      message.success(`Tracking successful`);
    } catch (error) {
      if (error.message) message.error('No Parcel Found');
    }
  };

  const columns = [
    {
      title: 'Name',
      search: false,
      dataIndex: 'name',
    },
    {
      title: 'Tracking ID',
      search: false,
      dataIndex: 'tracking_id',
    },
    {
      title: 'Sender',
      search: false,
      dataIndex: 'sender',
      render: (data, _) => <p>{data.name}</p>,
    },
    {
      title: 'Receiver',
      search: false,
      dataIndex: 'receiver',
      render: (data, _) => <p>{data.name}</p>,
    },
    {
      title: 'Action',
      dataIndex: 'option',
      valueType: 'option',
      render: (_, record) => [
        <Button
          key="track"
          type="primary"
          onClick={() => {
            handleSubmit({ value: record.id, type: 'id' });
          }}
        >
          Track
        </Button>,
      ],
    },
  ];

  return (
    <div
      style={{
        maxWidth: 1440,
        margin: 'auto',
        width: '80%',
        backgroundImage: 'https://gw.alipayobjects.com/zos/rmsportal/TVYTbAXWheQpRcWDaDMu.svg',
      }}
    >
      <ProForm
        form={form}
        layout="vertical"
        name="form_in_modal"
        onFinish={(data) => {
          handleSubmit(data, true);
        }}
        style={{
          margin: 'auto',
          marginTop: 48,
          backgroundColor: '#fff',
        }}
        submitter={{
          render: (props, doms) => {
            return [
              <Button
                type="primary"
                key="submit"
                style={{ margin: 16 }}
                onClick={() => props.form?.submit?.()}
              >
                Submit
              </Button>,
            ];
          },
        }}
      >
        <Row gutter={16}>
          <Col span={10}>
            <ProFormSelect
              name="type"
              label="Input Type"
              rules={[
                {
                  required: true,
                  message: 'You Must select an option',
                },
              ]}
              placeholder="Select option"
              options={[
                { label: 'Phone', value: 'phone' },
                { label: 'Tracking ID', value: 'id' },
              ]}
            />
          </Col>
          <Col span={10}>
            <ProFormText
              rules={[
                {
                  required: true,
                  message: 'You must add first name.',
                },
              ]}
              label="Value"
              name="value"
            />
          </Col>
        </Row>
      </ProForm>
      {parcels.length > 0 && <Table rowKey="id" dataSource={[...parcels]} columns={columns} />}

      <Steps progressDot direction="vertical" current={1000}>
        {tracking.map((data) => (
          <Step
            key={data.status}
            title={data.branch.name}
            description={formatDate(data.timestamp)}
          />
        ))}
      </Steps>
    </div>
  );
};

export default EntryForm;
