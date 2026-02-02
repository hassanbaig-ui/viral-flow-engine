import { AbsoluteFill, Video, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import React from "react";
import { z } from "zod";

// Define props validation
export const myCompSchema = z.object({
    clipIndex: z.number(),
    videoUrl: z.string(),
    startTime: z.number(),
    endTime: z.number(),
    title: z.string(),
    transcript: z.string(),
});

export const ViralComposition: React.FC<z.infer<typeof myCompSchema>> = ({
    clipIndex,
    videoUrl,
    startTime,
    endTime,
    title,
    transcript
}) => {
    const frame = useCurrentFrame();
    const { width, height, fps } = useVideoConfig();

    // Determine assets based on index or just use the passed URL?
    // We need to have the file locally for 'Video' component usually, OR use a remote URL.
    // videoUrl is remote (YouTube). Remotion <Video> supports remote URLs.
    // However, we want to clip it.
    // We can use 'startFrom' and 'endAt' props in Video if supported, or just offset startFrom.
    // <Video startFrom={startTime * fps} ... />

    // B-Roll: Alternate based on index
    const bRolls = [
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", // Placeholder High-end
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
    ];
    const bRollSrc = bRolls[clipIndex % bRolls.length];

    // Transformation
    const scale = 1.05;
    const hueRotate = frame % 360; // 1 degree static or rotating? "1% Hue-Rotate". 
    // 1% of 360 is 3.6deg. "1% Hue-Rotate" implies a static small shift to bypass hashing.
    const staticHue = "3.6deg";

    return (
        <AbsoluteFill style={{ backgroundColor: "black" }}>
            {/* Bottom Layer: Abstract B-Roll */}
            <AbsoluteFill style={{ zIndex: 0, height: "50%", top: "50%" }}>
                <Video
                    source={bRollSrc}
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        filter: "brightness(0.5)",
                    }}
                    loop
                    muted
                />
            </AbsoluteFill>

            {/* Top Layer: Main Clip */}
            <AbsoluteFill style={{ zIndex: 1, height: "50%", top: "0%" }}>
                <Video
                    source={videoUrl}
                    startFrom={Math.floor(startTime * fps)}
                    endAt={Math.floor(endTime * fps)}
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        transform: `scale(${scale})`,
                        filter: `hue-rotate(${staticHue})`,
                    }}
                />
            </AbsoluteFill>

            {/* Overlay / Divider */}
            <div style={{
                position: 'absolute',
                top: '50%',
                width: '100%',
                height: '4px',
                backgroundColor: 'white',
                zIndex: 2
            }} />

            {/* Kinetic Captions (Mocked for now as we don't have accurate word-timestamps in config yet) */}
            <AbsoluteFill style={{ zIndex: 3, justifyContent: 'center', alignItems: 'center', top: '25%' }}>
                <div style={{
                    fontFamily: "Montserrat",
                    fontSize: 60,
                    color: "white",
                    fontWeight: "bold",
                    textTransform: "uppercase",
                    textAlign: "center",
                    textShadow: "0px 0px 10px rgba(0,0,0,0.8)",
                    padding: 20
                }}>
                    {title}
                </div>
            </AbsoluteFill>
        </AbsoluteFill>
    );
};
