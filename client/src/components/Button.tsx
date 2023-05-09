import React from 'react';

interface IProps {
    text: string
    onPress?: () => void
}

const  Button : React.FC<IProps> = ({ text, onPress }) => {
    return(
        <div className='button'>
            <button className='btn-component' onClick={onPress}>
                {text}
            </button>
        </div>
    )
}

export default Button;