import { Composition } from 'remotion';
import { MyComposition, myCompSchema } from './Composition';

export const RemotionRoot: React.FC = () => {
    return (
        <>
            <Composition
                id="Root"
                component={MyComposition}
                durationInFrames={30 * 60} // Default 60 seconds at 30fps
                fps={30}
                width={1080}
                height={1920}
                defaultProps={{
                    clipUrl: '',
                    title: 'VIRAL CLIP'
                }}
                schema={myCompSchema}
            />
        </>
    );
};
