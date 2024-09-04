import React, { useState, FormEvent, ChangeEvent } from 'react';

interface FormProps<T> {
    initialValues: T;
    onSubmit: (values: T) => void;
    children: (props: {
        values: T;
        handleChange: (e: ChangeEvent<HTMLInputElement>) => void;
        handleSubmit: (e: FormEvent) => void;
    }) => React.ReactNode;
}

function Form<T>({ initialValues, onSubmit, children }: FormProps<T>) {
    const [values, setValues] = useState<T>(initialValues);

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setValues({ ...values, [name]: value });
    };

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        onSubmit(values);
    };

    return (
        <form onSubmit={handleSubmit}>
            {children({ values, handleChange, handleSubmit })}
        </form>
    );

}

export default Form;