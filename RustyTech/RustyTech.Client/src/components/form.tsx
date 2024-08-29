import React, { useState, FormEvent, ChangeEvent } from 'react';

interface FormProps<T> {
    initialValues: T;
    validate?: (values: T) => Partial<T>;
    onSubmit: (values: T) => void;
    children: (props: {
        values: T;
        errors: Partial<T>;
        handleChange: (e: ChangeEvent<HTMLInputElement>) => void;
        handleSubmit: (e: FormEvent) => void;
    }) => React.ReactNode;
}

function Form<T>({ initialValues, validate, onSubmit, children }: FormProps<T>) {
    const [values, setValues] = useState<T>(initialValues);
    const [errors, setErrors] = useState<Partial<T>>({});

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setValues({ ...values, [name]: value });
    };

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        const validationErrors = validate ? validate(values) : {};
        setErrors(validationErrors);
        if (Object.keys(validationErrors).length === 0) {
            onSubmit(values);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            {children({ values, errors, handleChange, handleSubmit })}
        </form>
    );

}

export default Form;