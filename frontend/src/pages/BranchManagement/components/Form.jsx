import React, { useEffect, useState } from 'react';
import ProForm, {
  ProFormDigit,
  ProFormGroup,
  ProFormMoney,
  ProFormRadio,
  ProFormSelect,
  ProFormSwitch,
  ProFormText,
  ProFormTextArea,
} from '@ant-design/pro-form';
import { message, Modal } from 'antd';
import { addBranch, updateBranch } from '../service';

const Form = (props) => {
  const { modalVisible, onSuccess, onCancel, name, title, values } = props;
  const [form] = ProForm.useForm();

  useEffect(() => form.setFieldsValue(values), [values]);

  const handleSubmit = async () => {
    try {
      const validatedData = await form.validateFields();
      const resp = await (values ? updateBranch : addBranch)({ ...validatedData, id: values?.id });
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

          <ProFormDigit
            rules={[
              {
                required: true,
                message: 'Must add value.',
              },
            ]}
            label="Estimated Processing Time"
            name="estimated_processing_time"
          />
          <ProFormMoney
            rules={[
              {
                required: true,
                message: 'Must add value.',
              },
            ]}
            customSymbol="৳"
            label="Estimated Processing Cost"
            name="estimated_processing_cost"
          />
        </ProForm.Group>
      </ProForm>
    </Modal>
  );
};

export default Form;
