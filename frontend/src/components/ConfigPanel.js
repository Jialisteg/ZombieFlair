import React, { useState } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Typography, 
  Slider,
  Grid,
  Card,
  CardContent,
  InputAdornment
} from '@mui/material';
import ApartmentIcon from '@mui/icons-material/Apartment';
import MeetingRoomIcon from '@mui/icons-material/MeetingRoom';
import Face5Icon from '@mui/icons-material/Face5';

const ConfigPanel = ({ onSetupBuilding, loading, simulationExists }) => {
  const [floors, setFloors] = useState(3);
  const [roomsPerFloor, setRoomsPerFloor] = useState(5);
  const [initialZombies, setInitialZombies] = useState(1);
  
  const handleFloorsChange = (event, newValue) => {
    setFloors(newValue);
  };
  
  const handleRoomsChange = (event, newValue) => {
    setRoomsPerFloor(newValue);
  };
  
  const handleZombiesChange = (event, newValue) => {
    setInitialZombies(newValue);
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSetupBuilding({
      floors,
      roomsPerFloor,
      initialZombies
    });
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>
                Tamaño del Edificio
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>
                  Número de Pisos
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Slider
                    value={floors}
                    onChange={handleFloorsChange}
                    valueLabelDisplay="auto"
                    step={1}
                    marks
                    min={1}
                    max={10}
                    disabled={loading}
                    sx={{ mr: 2, flexGrow: 1 }}
                  />
                  <TextField
                    value={floors}
                    onChange={(e) => {
                      const val = parseInt(e.target.value);
                      if (!isNaN(val) && val >= 1 && val <= 10) {
                        setFloors(val);
                      }
                    }}
                    type="number"
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <ApartmentIcon />
                        </InputAdornment>
                      ),
                      inputProps: { 
                        min: 1, 
                        max: 10
                      }
                    }}
                    disabled={loading}
                    size="small"
                    sx={{ width: '120px' }}
                  />
                </Box>
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>
                  Habitaciones por Piso
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Slider
                    value={roomsPerFloor}
                    onChange={handleRoomsChange}
                    valueLabelDisplay="auto"
                    step={1}
                    marks
                    min={1}
                    max={10}
                    disabled={loading}
                    sx={{ mr: 2, flexGrow: 1 }}
                  />
                  <TextField
                    value={roomsPerFloor}
                    onChange={(e) => {
                      const val = parseInt(e.target.value);
                      if (!isNaN(val) && val >= 1 && val <= 10) {
                        setRoomsPerFloor(val);
                      }
                    }}
                    type="number"
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <MeetingRoomIcon />
                        </InputAdornment>
                      ),
                      inputProps: { 
                        min: 1, 
                        max: 10
                      }
                    }}
                    disabled={loading}
                    size="small"
                    sx={{ width: '120px' }}
                  />
                </Box>
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>
                  Zombies Iniciales
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Slider
                    value={initialZombies}
                    onChange={handleZombiesChange}
                    valueLabelDisplay="auto"
                    step={1}
                    marks
                    min={0}
                    max={Math.min(floors * roomsPerFloor, 20)}
                    disabled={loading}
                    sx={{ mr: 2, flexGrow: 1 }}
                  />
                  <TextField
                    value={initialZombies}
                    onChange={(e) => {
                      const val = parseInt(e.target.value);
                      const maxZombies = Math.min(floors * roomsPerFloor, 20);
                      if (!isNaN(val) && val >= 0 && val <= maxZombies) {
                        setInitialZombies(val);
                      }
                    }}
                    type="number"
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Face5Icon />
                        </InputAdornment>
                      ),
                      inputProps: { 
                        min: 0, 
                        max: Math.min(floors * roomsPerFloor, 20)
                      }
                    }}
                    disabled={loading}
                    size="small"
                    sx={{ width: '120px' }}
                  />
                </Box>
              </Box>
              
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Vista previa: {floors} pisos, {roomsPerFloor} habitaciones por piso, {initialZombies} zombies
                </Typography>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Tamaño total del edificio: {floors * (roomsPerFloor + 1)} habitaciones (incluyendo escaleras)
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      
        <Grid item xs={12}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            disabled={loading}
            sx={{ mt: 1 }}
          >
            {simulationExists ? 'Reiniciar y Crear Nuevo Edificio' : 'Crear Edificio'}
          </Button>
          
          {simulationExists && (
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block', textAlign: 'center' }}>
              Advertencia: Esto reiniciará la simulación actual
            </Typography>
          )}
        </Grid>
      </Grid>
    </form>
  );
};

export default ConfigPanel; 