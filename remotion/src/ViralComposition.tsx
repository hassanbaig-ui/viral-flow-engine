import { AbsoluteFill, Video, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import React from "react";

// Mock captions data (in a real app, this would come from a transcription service)
const CAPTIONS = [
    { start: 0, end: 30, text: "This" },
    { start: 30, end: 60, text: "is" },
    { start: 60, end: 90, text: "the" },
    { start: 90, end: 120, text: "secret" },
    { start: 120, end: 150, text: "to" },
    { start: 150, end: 180, text: "success." },
];

export const ViralComposition: React.FC = () => {
    const frame = useCurrentFrame();
    const { width, height, fps } = useVideoConfig();

    // Assets (assuming they are in public/ or imported, but for Remotion 'src' can be a path)
    // We will use the assets downloaded to 'assets/' folder.
    // In Remotion, using local files outside 'public' or 'src' can be tricky with Webpack.
    // Usually we import them or put them in public.
    // For this implementation, we will assume they are served or we use absolute paths if running locally,
    // but for GitHub Actions, we should put them in 'public/assets' or similar.
    // The scout_clips.py puts them in 'assets/'. We should ensure the build process sees them.
    // For now, I'll link to files assuming they are available.

    // Note: In a real Remotion project, you'd use 'staticFile()' from @remotion/paths or imports.
    // I'll assume they are available at runtime.
    const mainClipSrc = "assets/clip1.mp4"; // Taking the first one for the comp
    const stockClipSrc = "assets/stock.mp4";

    // Filters
    // Pixel-Shift: 105% Scale
    const scale = 1.05;

    // Hue-Shift: 1% (approx 3.6 degrees)
    const hueRotate = "3.6deg";

    // Kinetic Captions
    const currentCaption = CAPTIONS.find(c => frame >= c.start && frame < c.end);

    return (
        <AbsoluteFill style={{ backgroundColor: "black" }}>
            {/* Bottom Layer: Dark Stock Footage */}
            <AbsoluteFill style={{ zIndex: 0 }}>
                <Video
                    source={stockClipSrc}
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        filter: "brightness(0.3)", // "High-quality dark stock"
                    }}
                    loop
                />
            </AbsoluteFill>

            {/* Top Layer: Main Clip */}
            <AbsoluteFill style={{ zIndex: 1, alignItems: 'center', justifyContent: 'center' }}>
                <Video
                    source={mainClipSrc}
                    style={{
                        // Layout: Center, Fit Width? 
                        // If it's a podcast (16:9), and we are 9:16, we fit width.
                        width: "100%",
                        // height: "auto", 
                        // Pixel Shift & Hue Shift
                        transform: `scale(${scale})`,
                        filter: `hue-rotate(${hueRotate})`,
                    }}
                />
            </AbsoluteFill>

            {/* Captions Layer */}
            <AbsoluteFill style={{ zIndex: 2, justifyContent: 'flex-end', paddingBottom: 150, alignItems: 'center' }}>
                {currentCaption && (
                    <div style={{
                        fontFamily: "Montserrat",
                        fontSize: 80,
                        color: "white",
                        fontWeight: "bold",
                        textTransform: "uppercase",
                        textAlign: "center",
                        textShadow: "0px 0px 10px rgba(0,0,0,0.8)",
                    }}>
                        {currentCaption.text}
                    </div>
                )}
            </AbsoluteFill>
        </AbsoluteFill>
    );
};
