import { AbsoluteFill, Video, DefaultProps } from 'remotion';
import { z } from 'zod';

export const myCompSchema = z.object({
    clipUrl: z.string(),
    title: z.string().optional(),
});

export const MyComposition: React.FC<z.infer<typeof myCompSchema>> = ({ clipUrl, title }) => {
    return (
        <AbsoluteFill style={{ backgroundColor: 'black' }}>
            {/* 
              Aggressive Transformation (Anti-Shadowban):
              - Pixel-Shift: Scale 105%
              - Hue-Shift: 1 deg (approx 1% shift)
            */}
            <AbsoluteFill
                style={{
                    transform: 'scale(1.05)',
                    filter: 'hue-rotate(1deg)'
                }}
            >
                {clipUrl ? (
                    <Video src={clipUrl} />
                ) : (
                    <div style={{ color: 'white', textAlign: 'center', top: '50%', position: 'absolute', width: '100%' }}>
                        No Clip URL Provided
                    </div>
                )}
            </AbsoluteFill>

            {/* Overlay Title/Subtitles Placeholder */}
            {title && (
                <div style={{
                    position: 'absolute',
                    bottom: 150,
                    width: '100%',
                    textAlign: 'center',
                    fontFamily: 'Montserrat',
                    fontSize: 60,
                    fontWeight: 'bold',
                    color: 'white',
                    textShadow: '0px 0px 10px black'
                }}>
                    {title.toUpperCase()}
                </div>
            )}
        </AbsoluteFill>
    );
};
