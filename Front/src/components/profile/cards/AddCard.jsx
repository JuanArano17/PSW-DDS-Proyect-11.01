import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, Typography } from '@mui/material';
import styles from '../../../styles/styles';

const AddCardForm = ({ onSave }) => {
  const [card, setCard] = useState({
    card_number: '',
    card_name: '',
    card_security_num: '',
    card_exp_date: '',
  });

  const [formValidity, setFormValidity] = useState({
    card_number: false,
    card_exp_date: false,
    card_security_num: false
  });

  const handleFieldValidation = (fieldId, value) => {
    switch (fieldId) {
      case "card_number":
        return /^\d{16}$/.test(value.replace(/\s+/g, '')); 
      case "card_exp_date":
        const currentDate = new Date();
        const inputDate = new Date(value);
        return inputDate > currentDate;
      case "card_security_num":
        return /^\d{3}$/.test(value);
      default:
        return false;
    }
  };

  useEffect(() => {
    setFormValidity({
      card_number: handleFieldValidation("card_number", card.card_number),
      card_exp_date: handleFieldValidation("card_exp_date", card.card_exp_date),
      card_security_num: handleFieldValidation("card_security_num", card.card_security_num)
    });
  }, [card]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCard(prevCard => ({
      ...prevCard,
      [name]: value,
    }));
    setFormValidity(prevValidity => ({
      ...prevValidity,
      [name]: handleFieldValidation(name, value)
    }));
  };

  const isFormValid = Object.values(formValidity).every(valid => valid);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isFormValid) {
      onSave(card);
    } else {
      console.error("Invalid form submission");
    }
  };

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
      <Typography variant="h6" gutterBottom>
        Add New Card
      </Typography>
      <TextField
        required
        fullWidth
        label="Card Number"
        name="card_number"
        margin="normal"
        value={card.card_number}
        onChange={handleChange}
        error={!formValidity.card_number}
        helperText={!formValidity.card_number ? "Card number must be 16 digits" : ""}
      />
      <TextField
        required
        fullWidth
        label="Card Name"
        name="card_name"
        margin="normal"
        value={card.card_name}
        onChange={handleChange}
      />
      <TextField
        required
        fullWidth
        label="CVV"
        name="card_security_num"
        margin="normal"
        inputProps={{ maxLength: 3 }}
        value={card.card_security_num}
        onChange={handleChange}
        error={!formValidity.card_security_num}
        helperText={!formValidity.card_security_num ? "CVV must be 3 digits" : ""}
      />
      <TextField
        required
        fullWidth
        label="Expiration Date"
        name="card_exp_date"
        margin="normal"
        type="date"
        InputLabelProps={{ shrink: true }}
        value={card.card_exp_date}
        onChange={handleChange}
        error={!formValidity.card_exp_date}
        helperText={!formValidity.card_exp_date ? "Expiration date must be later than today." : ""}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        sx={{...styles.greenRoundedButton, mt: 3}}
        disabled={!isFormValid}
      >
        Add Card
      </Button>
    </Box>
  );
};

export default AddCardForm;