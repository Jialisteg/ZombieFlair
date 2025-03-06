import React from 'react';
import { 
  Box, 
  Grid, 
  Typography, 
  LinearProgress, 
  Divider, 
  Chip,
  Card,
  CardContent
} from '@mui/material';
import { 
  Chart as ChartJS, 
  ArcElement, 
  Tooltip as ChartTooltip, 
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
} from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';

// Función para formatear el número de habitación
const formatRoomNumber = (floorIndex, roomNumber) => {
  // Sumamos 1 al índice del piso para que empiece en 1
  const floorNumber = floorIndex + 1;
  // Para habitaciones normales, usamos el formato piso + número secuencial
  return `${floorNumber}${roomNumber.toString().padStart(2, '0')}`;
};

// Register Chart.js components
ChartJS.register(
  ArcElement, 
  ChartTooltip, 
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
);

const StatsPanel = ({ data }) => {
  if (!data) {
    return (
      <Box sx={{ textAlign: 'center', p: 2 }}>
        <Typography>No hay estadísticas disponibles</Typography>
      </Box>
    );
  }

  // Extract data for charts
  const totalRooms = data.total_rooms || 0;
  const infestedRooms = data.infested_rooms || 0;
  const cleanRooms = totalRooms - infestedRooms;
  const infestedPercentage = totalRooms > 0 ? (infestedRooms / totalRooms) * 100 : 0;
  
  // Floor-wise infestation data for bar chart
  const floorLabels = [];
  const floorInfestation = [];
  const floorTotals = [];
  
  if (data.building && Array.isArray(data.building)) {
    data.building.forEach((floor, index) => {
      floorLabels.push(`Piso ${index}`);
      
      const totalRoomsInFloor = floor.length;
      const infestedRoomsInFloor = floor.filter(room => room.has_zombies).length;
      
      floorInfestation.push(infestedRoomsInFloor);
      floorTotals.push(totalRoomsInFloor);
    });
  }
  
  // Pie chart data
  const pieData = {
    labels: ['Habitaciones Limpias', 'Habitaciones Infestadas'],
    datasets: [
      {
        data: [cleanRooms, infestedRooms],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 99, 132, 0.6)'
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)'
        ],
        borderWidth: 1,
      },
    ],
  };
  
  // Bar chart data
  const barData = {
    labels: floorLabels,
    datasets: [
      {
        label: 'Habitaciones Infestadas',
        data: floorInfestation,
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
      {
        label: 'Habitaciones Limpias',
        data: floorTotals.map((total, index) => total - floorInfestation[index]),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      }
    ],
  };
  
  // Bar chart options
  const barOptions = {
    responsive: true,
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
        beginAtZero: true,
      },
    },
    plugins: {
      title: {
        display: true,
        text: 'Infestación por Piso'
      }
    }
  };

  return (
    <Grid container spacing={3}>
      {/* Current turn */}
      <Grid item xs={6} md={3}>
        <Card sx={{ height: '100%' }}>
          <CardContent>
            <Typography variant="overline" color="text.secondary">
              Turno Actual
            </Typography>
            <Typography variant="h4" component="div" sx={{ mt: 1 }}>
              {data.turn || 0}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      
      {/* Infestation Percentage */}
      <Grid item xs={6} md={3}>
        <Card sx={{ height: '100%' }}>
          <CardContent>
            <Typography variant="overline" color="text.secondary">
              Infestación
            </Typography>
            <Typography variant="h4" component="div" sx={{ mt: 1 }}>
              {infestedPercentage.toFixed(1)}%
            </Typography>
            <Box sx={{ width: '100%', mt: 1 }}>
              <LinearProgress 
                variant="determinate" 
                value={infestedPercentage} 
                color={infestedPercentage > 75 ? "error" : infestedPercentage > 50 ? "warning" : "success"}
              />
            </Box>
          </CardContent>
        </Card>
      </Grid>
      
      {/* Game Status */}
      <Grid item xs={6} md={3}>
        <Card sx={{ height: '100%' }}>
          <CardContent>
            <Typography variant="overline" color="text.secondary">
              Estado
            </Typography>
            <Box sx={{ mt: 1 }}>
              <Chip 
                label={data.game_over ? "Juego Terminado" : "En Progreso"} 
                color={data.game_over ? "error" : "success"} 
                variant="outlined"
              />
            </Box>
            {data.game_over && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                {data.game_over_reason === 'practicante_capturado' 
                  ? 'Practicante capturado' 
                  : 'Todas las habitaciones infestadas'}
              </Typography>
            )}
          </CardContent>
        </Card>
      </Grid>
      
      {/* Zombie Generation */}
      <Grid item xs={6} md={3}>
        <Card sx={{ height: '100%' }}>
          <CardContent>
            <Typography variant="overline" color="text.secondary">
              Generación de Zombies
            </Typography>
            <Box sx={{ mt: 1 }}>
              <Chip 
                label={data.zombie_generation_enabled ? "Activada" : "Desactivada"} 
                color={data.zombie_generation_enabled ? "warning" : "info"} 
                variant="outlined"
              />
            </Box>
          </CardContent>
        </Card>
      </Grid>
      
      {/* Infested vs Clean Rooms Pie Chart */}
      <Grid item xs={12} md={6}>
        <Card sx={{ height: '100%' }}>
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>
              Estado de las Habitaciones
            </Typography>
            <Box sx={{ height: 220, display: 'flex', justifyContent: 'center' }}>
              <Pie data={pieData} options={{ maintainAspectRatio: false }} />
            </Box>
          </CardContent>
        </Card>
      </Grid>
      
      {/* Floor-wise infestation Bar Chart */}
      <Grid item xs={12} md={6}>
        <Card sx={{ height: '100%' }}>
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>
              Infestación por Piso
            </Typography>
            <Box sx={{ height: 220 }}>
              <Bar data={barData} options={barOptions} />
            </Box>
          </CardContent>
        </Card>
      </Grid>
      
      {/* Practicante Information */}
      {data.practicante && (
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="subtitle1" gutterBottom>
                Ubicación del Practicante
              </Typography>
              <Typography variant="body1">
                El practicante se encuentra actualmente en la habitación {formatRoomNumber(data.practicante.floor, data.practicante.room)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      )}
    </Grid>
  );
};

export default StatsPanel; 