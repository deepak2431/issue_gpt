import React, { ChangeEvent } from 'react';

interface IProps {
    type: string
    id: string
    labelName: string
    value: string
    onInputChange: (e:ChangeEvent<HTMLInputElement>) => void
}

const  InputForm : React.FC<IProps> = ( { type, id, labelName, value, onInputChange} ) => {
    return(
        <div className='input_form'>
            <label className='input_label' htmlFor={id}>{labelName}</label>
            <input className='input_box' type={type} id={id} onChange={onInputChange} value={value}></input>
        </div>
    )
}

export default InputForm;