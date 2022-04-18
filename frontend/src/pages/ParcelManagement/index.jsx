import { PlusOutlined } from '@ant-design/icons';
import { Button, Drawer, message, Modal, Popconfirm } from 'antd';
import { useState, useRef } from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import ProTable from '@ant-design/pro-table';
import ProDescriptions from '@ant-design/pro-descriptions';
import { deleteParcel, getParcels, updateParcel } from './service';
import Form from './components/Form';
import { useModel } from 'umi';

const TableList = () => {
  const { initialState } = useModel('@@initialState');
  const { currentUser } = initialState || {};
  const [showForm, setShowForm] = useState(false);
  const [showDetail, setShowDetail] = useState(false);

  const actionRef = useRef();
  const [currentRow, setCurrentRow] = useState();

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [modalData, setModalData] = useState({});

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
    actionRef.current?.reload();
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    actionRef.current?.reload();
  };

  const handleUpdate = async (id, delivered, record) => {
    try {
      const data = { id: id };
      if (delivered) {
        data['current_tracking_status'] = 'delivered';
        data['parcel_on_return'] = record.parcel_on_return;
      } else {
        data['current_tracking_status'] = 'failed';
        data['parcel_on_return'] = true;
      }
      const resp = await updateParcel(data);
      if (!resp.success) throw resp;
      message.success(`Receive successful`);
    } catch (error) {
      if (error.message) message.error(error.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      const resp = await deleteParcel(id);
      if (!resp.success) throw resp;
      message.success(`Deleted successful`);
    } catch (error) {
      if (error.message) message.error('Invalid Request');
    }
  };

  const columns = [
    {
      title: 'Tracking ID',
      search: false,
      dataIndex: 'tracking_id',
    },
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
      title: 'Source Branch',
      search: false,
      dataIndex: 'source_branch',
      render: (data, _) => <p>{data.name}</p>,
    },
    {
      title: 'Destination Branch',
      search: false,
      dataIndex: 'destination_branch',
      render: (data, _) => <p>{data.name}</p>,
    },
    {
      title: 'Current Branch',
      search: false,
      dataIndex: 'current_branch_object',
      render: (data, _) => <p>{data.name}</p>,
    },
    {
      title: 'Status',
      search: false,
      dataIndex: 'current_tracking_status',
    },
    {
      title: 'Delivery',
      dataIndex: 'option',
      valueType: 'option',
      render: (_, record) =>
        record.current_tracking_status == 'delivered' ? (
          'Delivered'
        ) : record.current_tracking_status == 'arrived' ? (
          <>
            <Button
              key="success"
              type="primary"
              onClick={() => {
                handleUpdate(record.id, true, record);
                handleSuccess();
              }}
            >
              Success
            </Button>
            <Button
              key="failed"
              type="danger"
              style={{ marginLeft: 16 }}
              onClick={() => {
                handleUpdate(record.id, false, record);
                handleSuccess();
              }}
            >
              Failed
            </Button>
          </>
        ) : (
          '-'
        ),
    },
    {
      title: 'Actions',
      dataIndex: 'option',
      valueType: 'option',
      render: (_, record) => [
        <Popconfirm
          key="delete"
          placement="topLeft"
          title={'Are you sure you wanna delete this parcel?'}
          onConfirm={() => {
            handleDelete(record.id);
            handleSuccess();
          }}
          okText="Yes"
          cancelText="No"
        >
          <Button type="danger">Delete</Button>
        </Popconfirm>,
      ],
    },
  ];

  const handleSuccess = async () => {
    actionRef.current?.reload();
  };

  const drawerColumns = columns.filter(
    (c) =>
      ((currentUser?.role == 'delivery_man' && c.title == 'Delivery') || c.title != 'Delivery') &&
      ((currentUser?.role == 'admin' && c.title == 'Actions') || c.title != 'Actions'),
  );

  return (
    <>
      <Modal
        key="modal"
        title="Basic Modal"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <p>Tracking Number: {modalData.tracking_id}</p>
        <p>Cost: {modalData.cost}</p>
      </Modal>
      <ProTable
        actionRef={actionRef}
        rowKey="id"
        key="table"
        search={{
          labelWidth: 120,
          searchText: 'Search',
        }}
        toolBarRender={() => [
          currentUser.role !== 'delivery_man' && (
            <Button
              type="primary"
              key="primary"
              onClick={() => {
                setShowForm(true);
              }}
            >
              <PlusOutlined /> New
            </Button>
          ),
        ]}
        request={getParcels}
        columns={drawerColumns}
        pagination={{
          pageSize: 10,
        }}
      />

      <Form
        modalVisible={!currentRow && showForm}
        name="Parcel"
        onSuccess={() => {
          handleSuccess();
          showModal();
        }}
        setData={setModalData}
        onCancel={() => {
          setShowForm(false);
        }}
      />
      <Form
        modalVisible={!!(showForm && currentRow)}
        name="Parcel"
        values={currentRow ? { ...currentRow, store: currentRow.store?.slug } : undefined}
        onSuccess={handleSuccess}
        onCancel={() => {
          setShowForm(false);
          setCurrentRow(undefined);
        }}
      />

      <Drawer
        width={600}
        visible={showDetail}
        onClose={() => {
          setCurrentRow(undefined);
          setShowDetail(false);
        }}
        closable={false}
      >
        {currentRow && (
          <ProDescriptions
            column={2}
            title={currentRow?.username}
            dataSource={currentRow}
            columns={drawerColumns}
          />
        )}
      </Drawer>
    </>
  );
};

export default TableList;
