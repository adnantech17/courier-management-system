import React, { useEffect, useState } from 'react';
import ProForm, { ProFormDigit, ProFormMoney, ProFormSelect } from '@ant-design/pro-form';
import { message, Modal } from 'antd';
import { branchLinkCreate, getBranchesForDropdown } from '../service';

const Form = (props) => {
  const { modalVisible, onSuccess, onCancel, name, title, values } = props;
  const [form] = ProForm.useForm();

  useEffect(() => form.setFieldsValue(values), [values]);

  const handleSubmit = async () => {
    try {
      const validatedData = await form.validateFields();
      const resp = await branchLinkCreate({ ...validatedData, id: values?.id });
      if (!resp.success) throw resp;
      onSuccess();
      message.success(`Branch Link added successfully`);
      form.resetFields();
      onCancel();
    } catch (error) {
      if (error.message) message.error(error.message);
    }
  };

  return (
    <Modal
      visible={modalVisible}
      title={'Create a new Link'}
      okText={'Submit'}
      cancelText="Cancel"
      onCancel={onCancel}
      onOk={handleSubmit}
    >
      <ProForm
        form={form}
        layout="vertical"
        name={`Create Link`}
        submitter={{
          render: (props, doms) => {
            return [];
          },
        }}
        initialValues={values}
      >
        <ProForm.Group size={'middle'}>
          <ProFormSelect
            name="from_branch"
            label="From"
            rules={[
              {
                required: true,
                message: 'You Must select an option',
              },
            ]}
            placeholder="Select option"
            request={getBranchesForDropdown}
          />

          <ProFormSelect
            name="to_branch"
            label="To"
            rules={[
              {
                required: true,
                message: 'You Must select an option',
              },
            ]}
            placeholder="Select option"
            request={getBranchesForDropdown}
          />

          <ProFormDigit
            rules={[
              {
                required: true,
                message: 'Must add value.',
              },
            ]}
            label="Shipping Time"
            name="shipping_time"
          />

          <ProFormMoney
            rules={[
              {
                required: true,
                message: 'Must add value.',
              },
            ]}
            customSymbol="৳"
            label="Shipping Cost"
            name="shipping_cost"
          />
        </ProForm.Group>
      </ProForm>
    </Modal>
  );
};

export default Form;
