import ProForm, { ProFormSelect, ProFormText } from '@ant-design/pro-form';
import { PageContainer } from '@ant-design/pro-layout';
import { Row, Col, message, Table, Button } from 'antd';
import { useState } from 'react';
import 'react-tagsinput/react-tagsinput.css';
import ReactTagsInput from 'react-tagsinput';
import { getBranchesForDropdown } from '@/pages/BranchManagement/service';
import { checkRouteParcel, routeParcel } from './service';

const EntryForm = () => {
  const [form] = ProForm.useForm();
  const [tags, setTags] = useState([]);
  const [products, setProducts] = useState([]);

  const handleChange = (pTags, changed) => {
    const newTags = [...new Set(pTags)];
    if (tags.length < newTags.length) {
      console.log(changed);
      checkRouteParcel({}, parseInt(changed[0])).then((res) => {
        if (res.success) {
          setTags(newTags);
          setProducts([...products, res.data]);
        } else message.error('Invalid ID');
      });
    } else if (tags.length > newTags.length) {
      setProducts(products.filter((prod) => prod.id !== parseInt(changed[0])));
      setTags(newTags);
    }
  };

  const handleSubmit = async (data) => {
    try {
      const subData = {
        serials: data.serials.join(','),
      };
      const resp = await routeParcel(subData);
      if (!resp.success) throw resp;
      message.success(`Route successful`);
    } catch (error) {
      if (error.message) message.error(error.message);
    }
  };

  const columns = [
    {
      title: 'Name',
      search: false,
      dataIndex: 'name',
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
      title: 'Next Branch',
      search: false,
      dataIndex: 'next_route',
      render: (data, _) => <p>{data ? data.name : '-'}</p>,
    },
  ];

  return (
    <PageContainer>
      <ProForm
        form={form}
        layout="vertical"
        name="form_in_modal"
        onFinish={(data) => {
          handleSubmit(data);
        }}
        style={{
          margin: 'auto',
          marginTop: 8,
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
        <div style={{ maxWidth: 1080, margin: 'auto', padding: 24 }}>
          <ProForm.Item name="serials" rules={[{ required: true, message: 'Must have serials' }]}>
            <ReactTagsInput
              value={tags}
              onChange={handleChange}
              inputProps={{ placeholder: 'Add serials' }}
            />
          </ProForm.Item>
        </div>
        <Table
          rowKey="id"
          search={{
            labelWidth: 120,
            searchText: 'Search',
          }}
          dataSource={[...products]}
          columns={columns}
          pagination={{
            pageSize: 10,
          }}
        />
      </ProForm>
    </PageContainer>
  );
};

export default EntryForm;
