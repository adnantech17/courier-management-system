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
import { message, Modal } from 'antd';
import { addUser, updateUser } from '../service';
import { getBranchesForDropdown } from '@/pages/BranchManagement/service';

const Form = (props) => {
  const { modalVisible, onSuccess, onCancel, name, title, values } = props;
  const [form] = ProForm.useForm();

  useEffect(() => form.setFieldsValue(values), [values]);

  const handleSubmit = async () => {
    try {
      const validatedData = await form.validateFields();
      const resp = await (values ? updateUser : addUser)({ ...validatedData, id: values?.id });
      console.log(resp);
      if (!resp.success) throw resp;
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
              message: 'You must add username.',
            },
          ]}
          label="Username"
          name="username"
        />
        <ProForm.Group size={'middle'}>
          <ProFormText
            rules={[
              {
                required: true,
                message: 'You must add first name.',
              },
            ]}
            label="Name"
            name="name"
          />

          <ProFormText
            rules={[
              {
                type: 'email',
                required: true,
                message: 'You must add email.',
              },
            ]}
            label="Email"
            name="email"
          />
        </ProForm.Group>
        {!values && (
          <ProFormText.Password
            rules={[
              {
                required: true,
                message: 'You must add password',
              },
            ]}
            label="Password"
            name="password"
          />
        )}

        <ProFormSelect
          name="role"
          label="Role"
          rules={[
            {
              required: true,
              message: 'Must select an option',
            },
          ]}
          placeholder="Select option"
          options={[
            { label: 'Delivery Man', value: 'delivery_man' },
            { label: 'Admin', value: 'admin' },
            { label: 'Office Staff', value: 'office_staff' },
          ]}
        />

        <ProFormSelect
          name="assigned_branch"
          label="Branch"
          rules={[
            {
              required: true,
              message: 'Must select an option',
            },
          ]}
          placeholder="Select option"
          request={getBranchesForDropdown}
        />
      </ProForm>
    </Modal>
  );
};

export default Form;
