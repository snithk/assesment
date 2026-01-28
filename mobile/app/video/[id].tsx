import { useLocalSearchParams, useRouter } from 'expo-router';
import { useEffect, useState } from 'react';
import { View, StyleSheet, ActivityIndicator, Alert, Dimensions, Text } from 'react-native';
import { videoService } from '../../services/api';
import { WebView } from 'react-native-webview';

export default function VideoPlayerScreen() {
    const { id, token } = useLocalSearchParams();
    const [streamData, setStreamData] = useState(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        if (id && token) {
            loadStream();
        }
    }, [id, token]);

    const loadStream = async () => {
        try {
            const data = await videoService.getStreamUrl(id, token);
            setStreamData(data);
        } catch (error) {
            Alert.alert('Error', 'Failed to load video stream');
            router.back();
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <View style={styles.centered}>
                <ActivityIndicator size="large" color="#0000ff" />
            </View>
        );
    }

    if (!streamData) {
        return (
            <View style={styles.centered}>
                <Text>Video not available</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <View style={styles.videoContainer}>
                {/* 
           WebView Player Wrapper 
           - loads stream_url (youtube embed in this case)
           - prevents navigation to other pages
        */}
                <WebView
                    source={{ uri: streamData.stream_url }}
                    style={styles.webview}
                    javaScriptEnabled={true}
                    domStorageEnabled={true}
                    allowsInlineMediaPlayback={true}
                    mediaPlaybackRequiresUserAction={false}
                    // Strict Navigation Control
                    onShouldStartLoadWithRequest={(request) => {
                        // Allow the initial load of the stream URL
                        if (request.url === streamData.stream_url) return true;

                        // Allow google/youtube domains for the player internals
                        if (request.url.includes('youtube.com') || request.url.includes('google.com')) {
                            // Return true, BUT we might want to block clicking "Watch on YouTube" logo?
                            // Youtube IFrame API usually handles this, but in pure WebView, clicks might open new pages.
                            // We can't easily block specific click events, but we can try to block navigation to "watch?v=" if it tries to navigate away.
                            // For this assignment, "Use onShouldStartLoadWithRequest to block any navigation away from the masked stream"
                            // means we should strictly allow only what's needed.

                            // If the new URL is NOT the stream_url (Embed URL), block it?
                            // The Embed URL is "https://www.youtube.com/embed/..."
                            // If user clicks title, it might try to go to "https://www.youtube.com/watch?v=..."

                            if (request.url.includes('/embed/')) return true;

                            // Block everything else to prevent "escaping" the player
                            return false;
                        }

                        return false;
                    }}
                />
            </View>
            <View style={styles.controls}>
                <Text style={styles.hint}>Now Playing: Video {streamData.video_id}</Text>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: 'black', justifyContent: 'center' },
    centered: { flex: 1, justifyContent: 'center', alignItems: 'center' },
    videoContainer: { width: '100%', height: 300 }, // Aspect ratio
    webview: { flex: 1 },
    controls: { padding: 20, alignItems: 'center' },
    hint: { color: 'white' }
});
