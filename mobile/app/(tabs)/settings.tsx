import { View, Text, Button, StyleSheet } from 'react-native';
import { authService } from '../../services/api';
import { useRouter } from 'expo-router';
import { useEffect, useState } from 'react';

interface User {
    name: string;
    email: string;
}

export default function Settings() {
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        loadUser();
    }, []);

    const loadUser = async () => {
        try {
            const data = await authService.me();
            setUser(data);
        } catch (e) {
            console.log(e);
        }
    };

    const handleLogout = async () => {
        await authService.logout();
        router.replace('/(auth)/login');
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Settings</Text>
            {user && (
                <View style={styles.userInfo}>
                    <Text style={styles.label}>Name: {user.name}</Text>
                    <Text style={styles.label}>Email: {user.email}</Text>
                </View>
            )}
            <Button title="Logout" onPress={handleLogout} color="red" />
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20, paddingTop: 50 },
    title: { fontSize: 26, fontWeight: 'bold', marginBottom: 30 },
    userInfo: { marginBottom: 30 },
    label: { fontSize: 18, marginBottom: 10 }
});
