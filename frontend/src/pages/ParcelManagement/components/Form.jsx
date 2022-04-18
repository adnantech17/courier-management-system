import React, { useEffect, useState } from 'react';
import ProForm, {
  ProFormDigit,
  ProFormGroup,
  ProFormRadio,
  ProFormSelect,
  ProFormSwitch,
  ProFormText,
  ProFormTextArea,
} from '@ant-design/pro-form';
import { Col, message, Modal, Row } from 'antd';
import { addParcel, updateParcel } from '../service';
import { getBranchesForDropdown } from '@/pages/BranchManagement/service';
import { useModel } from 'umi';

const Form = (props) => {
  const { initialState } = useModel('@@initialState');
  const { currentUser } = initialState || {};
  const { modalVisible, onSuccess, onCancel, name, title, values, setData } = props;
  const [form] = ProForm.useForm();

  useEffect(() => form.setFieldsValue(values), [values]);

  const handleSubmit = async () => {
    try {
      const validatedData = await form.validateFields();
      const data = {
        name: validatedData.name,
        source_address: {
          detailed_address: validatedData.detailed_address_source,
          branch: validatedData.branch_source,
        },
        destination_address: {
          detailed_address: validatedData.detailed_address_dest,
          branch: validatedData.branch_dest,
        },
        sender: {
          name: validatedData.sender_name,
          contact_number: validatedData.sender_contact,
        },
        receiver: {
          name: validatedData.receiver_name,
          contact_number: validatedData.receiver_contact,
        },
        current_tracking_status: 'pending',
        parcel_on_return: false,
      };
      const resp = await (values ? updateParcel : addParcel)({ ...data, id: values?.id });
      if (!resp.success) throw resp;
      setData(resp.data);
      onSuccess();
      message.success(`${values ? 'Edited' : 'Added'} successfully`);
      form.resetFields();
      onCancel();
    } catch (error) {
      if (error.message) message.error(error.message);
    }
  };

  return (
    <Modal
      visible={modalVisible}
      title={title || (values ? `Edit ${name}` : `Create a new ${name}`)}
      okText={'Submit'}
      cancelText="Cancel"
      onCancel={onCancel}
      onOk={handleSubmit}
      width="1080px"
    >
      <ProForm
        form={form}
        layout="vertical"
        name={`${name}__${values ? 'edit' : 'create'}`}
        submitter={{
          render: (props, doms) => {
            return [];
          },
        }}
        initialValues={values}
      >
        <ProFormText
          rules={[
            {
              required: true,
              message: 'You must enter value.',
            },
          ]}
          label="Parcel Name"
          name="name"
        />
        <h3>Source Address</h3>
        <Row gutter={16}>
          <Col span={12}>
            <ProFormTextArea
              rules={[
                {
                  required: true,
                  message: 'You must enter value.',
                },
              ]}
              label="Detailed Address"
              name="detailed_address_source"
            />
          </Col>
          <Col span={12}>
            <ProFormSelect
              name="branch_source"
              label="Branch"
              rules={[
                {
                  required: true,
                  message: 'You Must select an option',
                },
              ]}
              placeholder="Select option"
              request={getBranchesForDropdown}
              disabled={currentUser.role === 'office_staff'}
              initialValue={{ value: currentUser.branch.id, label: currentUser.branch.name }}
            />
          </Col>
        </Row>

        <h3>Destination Address</h3>
        <Row gutter={16}>
          <Col span={12}>
            <ProFormTextArea
              rules={[
                {
                  required: true,
                  message: 'You must enter value.',
                },
              ]}
              label="Detailed Address"
              name="detailed_address_dest"
            />
          </Col>

          <Col span={12}>
            <ProFormSelect
              name="branch_dest"
              label="Branch"
              rules={[
                {
                  required: true,
                  message: 'You Must select an option',
                },
              ]}
              placeholder="Select option"
              request={getBranchesForDropdown}
            />
          </Col>
        </Row>

        <h3>Sender Details</h3>
        <Row gutter={16}>
          <Col span={12}>
            <ProFormText
              rules={[
                {
                  required: true,
                  message: 'You must enter value.',
                },
              ]}
              label="Name"
              name="sender_name"
            />
          </Col>
          <Col span={12}>
            <ProFormText
              rules={[
                {
                  required: true,
                  message: 'You must enter value.',
                },
              ]}
              label="Contact Number"
              name="sender_contact"
            />
          </Col>
        </Row>

        <h3>Receiver Details</h3>
        <Row gutter={16}>
          <Col span={12}>
            <ProFormText
              rules={[
                {
                  required: true,
                  message: 'You must enter value.',
                },
              ]}
              label="Name"
              name="receiver_name"
            />
          </Col>
          <Col span={12}>
            <ProFormText
              rules={[
                {
                  required: true,
                  message: 'You must enter value.',
                },
              ]}
              label="Contact Number"
              name="receiver_contact"
            />
          </Col>
        </Row>
      </ProForm>
    </Modal>
  );
};

export default Form;
