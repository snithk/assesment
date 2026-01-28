import { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, Image, StyleSheet, ActivityIndicator } from 'react-native';
import { videoService } from '../../services/api';
import { useRouter } from 'expo-router';

export default function Dashboard() {
    const [videos, setVideos] = useState([]);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        loadVideos();
    }, []);

    const loadVideos = async () => {
        try {
            const data = await videoService.getDashboard();
            setVideos(data);
        } catch (error) {
            console.log('Error loading videos', error);
        } finally {
            setLoading(false);
        }
    };

    const renderItem = ({ item }: { item: any }) => (
        <TouchableOpacity
            style={styles.card}
            onPress={() => router.push({ pathname: '/video/[id]', params: { id: item.id, token: item.playback_token } })}
        >
            <Image source={{ uri: item.thumbnail_url }} style={styles.thumbnail} />
            <View style={styles.info}>
                <Text style={styles.title}>{item.title}</Text>
                <Text style={styles.description}>{item.description}</Text>
            </View>
        </TouchableOpacity>
    );

    return (
        <View style={styles.container}>
            <Text style={styles.header}>Dashboard</Text>
            {loading ? (
                <ActivityIndicator size="large" />
            ) : (
                <FlatList
                    data={videos}
                    renderItem={renderItem}
                    keyExtractor={(item: any) => item.id}
                    style={styles.list}
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5', padding: 10 },
    header: { fontSize: 28, fontWeight: 'bold', marginVertical: 20 },
    list: { flex: 1 },
    card: { backgroundColor: 'white', borderRadius: 10, overflow: 'hidden', marginBottom: 20, elevation: 3 },
    thumbnail: { width: '100%', height: 200 },
    info: { padding: 15 },
    title: { fontSize: 18, fontWeight: 'bold' },
    description: { fontSize: 14, color: '#666', marginTop: 5 }
});
