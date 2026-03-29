import {
    Card,
    CardContent,
    Box,
    FormGroup,
    FormControlLabel,
    Checkbox, FormControl, Button
} from "@mui/material";
import {useState} from "react";
import {useNavigate} from "react-router-dom";


const IntroForm = () => {

    const [formState, setFormState] = useState({
        btcusdt: true,
        ethusdt: false,
        solusdt: false
    })
    const handleChange = (event) => {

        setFormState({...formState, [event.target.name]: event.target.checked})
    }

    const navigate = useNavigate();

    const handleButtonClick = (event) => {
        event.preventDefault();
        event.stopPropagation();

        let cryptoSymbolsToTrack = []

        Object.entries(formState).forEach(([key, value]) => {
            if (value) {
                cryptoSymbolsToTrack.push(key)
            }
        })

        navigate("/dashboard", {state: {cryptoSymbols: cryptoSymbolsToTrack}})

    }
    return (
        <Card sx={{minWidth: 275, maxWidth: 500, margin: "auto", marginTop: 10, backgroundColor: "#f5f5f5"}}>
            <CardContent>
                <h1>Crypto Tracker</h1>
                <Box sx={{display: "flex", flexDirection: "column"}}>
                    <FormControl style={{marginBottom: 20}}>
                        <p style={{textAlign: "left"}}>
                            Select Cryptocurrencies
                        </p>
                        <FormGroup>
                            <FormControlLabel
                                control={
                                    <Checkbox name={"btcusdt"}
                                              onChange={handleChange}
                                              checked={formState.btcusdt}
                                    />
                                }
                                label="Bitcoin (BTCUSDT)"
                                style={{maxWidth: "fit-content"}}
                            />
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        name={"ethusdt"}
                                        onChange={handleChange}
                                        checked={formState.ethusdt}
                                    />
                                }
                                style={{maxWidth: "fit-content"}}
                                label="Ethereum (ETHUSDT)"
                            />
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        name={"solusdt"}
                                        onChange={handleChange}
                                        checked={formState.solusdt}
                                    />
                                }
                                style={{maxWidth: "fit-content"}}
                                label="Solana (SOLUSDT)"
                            />
                        </FormGroup>
                    </FormControl>
                    <Button name={"Track"} onClick={handleButtonClick} variant="contained">
                        Track Now
                    </Button>
                </Box>
            </CardContent>
        </Card>
    )
}

export default IntroForm;
