import {Box, Card, CardContent, Container, Skeleton} from "@mui/material";
import {useLocation, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import WebSocketClient from "data/websocket";


const Dashboard = () => {
    const location = useLocation();
    // Access the state object
    const {state} = location
    const cryptoSymbols = state?.cryptoSymbols

    const navigate = useNavigate();

    const [showUI, setShowUI] = useState(false)
    const [data, setData] = useState({})
    const [ws, setWs] = useState(null)


    useEffect(() => {
        let newWebSocket = null;
        const openConnection = async () => {
            try {
                newWebSocket = new WebSocketClient(`${process.env.REACT_APP_WS_URI}/crypto/track`)
                setWs(newWebSocket)
            } catch (e) {
                console.error(e) //todo: show error popup
            }

        }

        if (!state || !cryptoSymbols) {
            navigate("/")
        } else {
            openConnection()
        }

        return () => {
            console.log("Closing WebSocket")
            const closeConnection = async () => {
                if (newWebSocket)
                    try {
                        await newWebSocket.socket.close()
                    } catch (e) {
                        console.error(e)
                    }

            }
            closeConnection()
        }
    }, [state, cryptoSymbols, navigate])


    if (ws !== null) {
        ws.socket.onopen = () => {
            ws.subscribe(cryptoSymbols)
        }

        ws.socket.onmessage = (event) => {
            let messageData = JSON.parse(event.data)

            if (messageData.type === "INFO") {
                setData({...data, [messageData.data.symbol.toLowerCase()]: messageData.data})

                if (Object.keys(data).length === cryptoSymbols.length) {
                    setShowUI(true)
                }
            }

        }

    }

    const DataRow = ({label, value}) => (
        <>
            <div style={{fontWeight: "bold"}}>{label}</div>
            <div>{value}</div>
        </>
    );

    const PercentChange = ({value}) => {
        const parsed = parseFloat(value);
        return (
            <div style={{color: parsed >= 0 ? "green" : "red"}}>
                {parsed.toFixed(4)}%
            </div>
        );
    };
    const Cards = data && Object.entries(data).map(([symbol, symbolData]) => {
        return (
            <Card key={symbol}>
                <CardContent>
                    <Box sx={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: 2, textAlign: "left"}}>
                        <DataRow label="Symbol" value={symbolData.symbol}/>
                        <DataRow label="Last Price" value={symbolData.last_price}/>
                        <DataRow label="24h Change" value={<PercentChange value={symbolData.percent_change}/>}/>
                        <DataRow label="Last Updated At" value={new Date(symbolData.timestamp).toLocaleString()}/>
                    </Box>
                </CardContent>
            </Card>
        )

    })

    const SkeletonComponents = cryptoSymbols && cryptoSymbols.map((symbol) => {
        return <Skeleton variant="rectangular" key={symbol}/>
    })

    return (
        <Container>
            <h1>Dashboard</h1>
            <div style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: 25}}>
                {showUI ? Cards : SkeletonComponents}
            </div>
        </Container>
    )
}

export default Dashboard;