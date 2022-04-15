import { PlusOutlined } from '@ant-design/icons';
import { Button, Drawer } from 'antd';
import { useState, useRef } from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import ProTable from '@ant-design/pro-table';
import ProDescriptions from '@ant-design/pro-descriptions';
import { getBranchEdges } from './service';
import Form from './components/Form';

const TableList = () => {
  const [showForm, setShowForm] = useState(false);
  const [showDetail, setShowDetail] = useState(false);

  const actionRef = useRef();
  const [currentRow, setCurrentRow] = useState();

  const columns = [
    {
      title: 'From Branch',
      search: false,
      dataIndex: 'from_branch_name',
      render: (data, _) => <p>{data.name}</p>,
    },
    {
      title: 'To Branch',
      search: false,
      dataIndex: 'to_branch_name',
      render: (data, _) => <p>{data.name}</p>,
    },
    {
      title: 'Shipping Time',
      search: false,
      dataIndex: 'shipping_time',
      render: (data, _) => <p>{data} hours</p>,
    },
    {
      title: 'Shipping Cost',
      search: false,
      dataIndex: 'shipping_cost',
      render: (data, _) => <p>&#2547;{data}</p>,
    },
    // {
    //   title: 'Actions',
    //   dataIndex: 'option',
    //   valueType: 'option',
    //   render: (_, record) => [
    //     <a
    //       key="config"
    //       onClick={() => {
    //         setCurrentRow(record);
    //         setShowForm(true);
    //       }}
    //     >
    //       Edit
    //     </a>,
    //   ],
    // },
  ];

  const handleSuccess = async () => {
    actionRef.current?.reload();
  };

  const drawerColumns = columns.filter((c) => c.title !== 'Actions');

  return (
    <PageContainer>
      <ProTable
        actionRef={actionRef}
        rowKey="id"
        search={{
          labelWidth: 120,
          searchText: 'Search',
        }}
        toolBarRender={() => [
          <Button
            type="primary"
            key="primary"
            onClick={() => {
              setShowForm(true);
            }}
          >
            <PlusOutlined /> New
          </Button>,
        ]}
        request={getBranchEdges}
        columns={columns}
        pagination={{
          pageSize: 10,
        }}
      />

      <Form
        modalVisible={!currentRow && showForm}
        name="Branch Link"
        onSuccess={handleSuccess}
        onCancel={() => {
          setShowForm(false);
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
    </PageContainer>
  );
};

export default TableList;